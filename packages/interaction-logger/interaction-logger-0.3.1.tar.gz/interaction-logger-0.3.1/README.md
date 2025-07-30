# Interaction Logger

A Django middleware for logging user interactions with your application.

## Features

- Logs user activity including request and response details
- Asynchronous logging to avoid impacting request-response cycle
- Works in both ASGI and WSGI environments
- Supports custom fields for tracking additional information

## Installation

```bash
pip install interaction-logger
```

## Configuration

Add the middleware to your Django settings:

```python
MIDDLEWARE = [
    # ... other middleware
    'interaction_logger.middleware.UserActivityMiddleware',
    # ... other middleware
]
```

## Usage

### Basic Usage

Once configured, the middleware will automatically log user activity for all requests except those to `/admin/`, `/static/`, and `/media/`.

### Custom Fields

You can add custom fields to track additional information. This is useful for tracking business-specific data or for debugging purposes.

```python
from interaction_logger.middleware import UserActivityMiddleware

# Track the user's browser information
def get_browser_info(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    if 'Chrome' in user_agent:
        return 'Chrome'
    elif 'Firefox' in user_agent:
        return 'Firefox'
    else:
        return 'Other'

UserActivityMiddleware.add_custom_field('browser', get_browser_info)

# Track a query parameter
UserActivityMiddleware.add_custom_field('source', lambda request: request.GET.get('source'))
```

The `add_custom_field` method takes two arguments:
1. `field_name`: The name of the custom field to track
2. `field_value_getter`: A function that takes a request object and returns the value to track

The function should handle any exceptions internally to avoid breaking the middleware.

See the [examples directory](examples/) for more examples of custom fields.

## Viewing Logs

User activity logs are stored in the database and can be viewed in the Django admin interface.

## License

MIT
