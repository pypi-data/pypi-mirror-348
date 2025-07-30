from django.db import models
from django.contrib.postgres.fields import JSONField


class UserActivity(models.Model):
    user = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    request_data = JSONField(null=True, blank=True)
    response_status = models.IntegerField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    response_message = models.TextField(null=True, blank=True)
    custom_fields = JSONField(null=True, blank=True, help_text="Custom fields that user wants to track")

    class Meta:
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
        ordering = ['-timestamp']

    def __str__(self):
        user_str = self.user if self.user else 'Anonymous'
        return f"{user_str} - {self.method} {self.path} ({self.timestamp})"
