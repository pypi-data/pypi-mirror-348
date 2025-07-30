import json
import asyncio
import sys
from functools import partial
from asgiref.sync import sync_to_async
from django.db import transaction
from .models import UserActivity

def run_async_in_py36(coro):
    """
    Helper function to mimic asyncio.run() in Python 3.6
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        # Cancel all running tasks
        if sys.version_info >= (3, 7, 0):
            tasks = asyncio.all_tasks(loop)
        else:
            tasks = asyncio.Task.all_tasks(loop)

        for task in tasks:
            task.cancel()

        # Run the event loop until all tasks are cancelled
        loop.run_until_complete(
            asyncio.gather(*tasks, return_exceptions=True)
        )

        # Close the loop
        loop.close()
        asyncio.set_event_loop(None)


class UserActivityMiddleware:
    # Dictionary to store custom fields that users want to track
    _custom_fields = {}
    # Function to determine the user value to be saved
    _user_getter = staticmethod(lambda request: request.user if getattr(request, 'user', None) and request.user.is_authenticated else None)

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def add_custom_field(cls, field_name, field_value_getter):
        """
        Add a custom field to track in the UserActivity log.

        Args:
            field_name (str): The name of the custom field to track.
            field_value_getter (callable): A function that takes a request object and returns the value to track.
                                          This function should handle any exceptions internally.

        Example:
            # Track the user's IP address in a custom field
            UserActivityMiddleware.add_custom_field('client_ip', lambda request: request.META.get('REMOTE_ADDR'))

            # Track a request header
            UserActivityMiddleware.add_custom_field('custom_header', lambda request: request.headers.get('X-Custom-Header'))

            # Track a value from the request body for POST requests
            def get_request_body_value(request):
                if request.method == 'POST' and hasattr(request, 'body'):
                    try:
                        body = json.loads(request.body.decode('utf-8'))
                        return body.get('some_field')
                    except:
                        return None
                return None

            UserActivityMiddleware.add_custom_field('body_value', get_request_body_value)
        """
        cls._custom_fields[field_name] = field_value_getter

    @classmethod
    def set_user_getter(cls, user_getter_func):
        """
        Set a custom function to determine the user value to be saved in the UserActivity log.

        Args:
            user_getter_func (callable): A function that takes a request object and returns the user value to save.
                                         This function should handle any exceptions internally.

        Example:
            # Save the user's email instead of the user object
            UserActivityMiddleware.set_user_getter(lambda request: request.user.email if request.user.is_authenticated else None)
        """
        cls._user_getter = staticmethod(user_getter_func)

    @staticmethod
    @sync_to_async
    def _create_user_activity(user, path, method, request_data, status_code, ip_address, user_agent, response_message, custom_fields=None):
        """Create a UserActivity record asynchronously"""
        UserActivity.objects.create(
            user=user,
            path=path,
            method=method,
            request_data=request_data,
            response_status=status_code,
            ip_address=ip_address,
            user_agent=user_agent,
            response_message=response_message,
            custom_fields=custom_fields
        )

    @staticmethod
    def _schedule_async_creation(user, path, method, request_data, status_code, ip_address, user_agent, response_message, custom_fields=None):
        """Schedule the async creation of a UserActivity record in a way that works in both ASGI and WSGI environments"""
        async_task = partial(
            UserActivityMiddleware._create_user_activity,
            user, path, method, request_data, status_code, ip_address, user_agent, response_message, custom_fields
        )

        try:
            # Try to get the current event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're in an async context (ASGI), schedule the task
                asyncio.ensure_future(async_task())
            else:
                # If we're not in an async context (WSGI), run the task in a new event loop
                if sys.version_info >= (3, 7):
                    # asyncio.run() is available in Python 3.7+
                    asyncio.run(async_task())
                else:
                    # Use our helper function for Python 3.6
                    run_async_in_py36(async_task())
        except RuntimeError:
            # If there's no event loop, create one and run the task
            if sys.version_info >= (3, 7):
                # asyncio.run() is available in Python 3.7+
                asyncio.run(async_task())
            else:
                # Use our helper function for Python 3.6
                run_async_in_py36(async_task())

    def __call__(self, request):
        request_data = None
        response = None
        response_message = None

        if not request.path.startswith(('/admin/', '/static/', '/media/')):
            if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                try:
                    request_data = json.loads(request.body.decode('utf-8'))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    request_data = None

            try:
                response = self.get_response(request)

            finally:
                status_code = getattr(response, 'status_code', 500)

                # Capture response content for non-successful responses
                if status_code not in [200, 201] and hasattr(response, 'content'):
                    try:
                        response_message = response.content.decode('utf-8')
                    except UnicodeDecodeError:
                        response_message = '<binary or undecodable response>'

                # Collect custom fields if any are defined
                custom_fields = None
                if self._custom_fields:
                    custom_fields = {}
                    for field_name, getter_func in self._custom_fields.items():
                        try:
                            custom_fields[field_name] = getter_func(request)
                        except Exception as e:
                            # Silently ignore errors in custom field getters
                            custom_fields[field_name] = f"Error: {str(e)}"

                # Use the user getter function to determine the user value
                try:
                    user_value = self._user_getter(request)
                except Exception as e:
                    user_value = "Error"

                # Schedule the UserActivity creation to run asynchronously
                transaction.on_commit(lambda: self._schedule_async_creation(
                    user=user_value,
                    method=request.method,
                    path=request.build_absolute_uri(),
                    request_data=request_data,
                    status_code=status_code,
                    ip_address=self._get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    response_message=response_message,
                    custom_fields=custom_fields
                ))

                return response
        else:
            response = self.get_response(request)

        return response

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
