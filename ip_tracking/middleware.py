from django.utils.deprecation import MiddlewareMixin
from .models import RequestLog
from django.utils import timezone


class IPLoggingMiddleware(MiddlewareMixin):
    """
    Middleware that logs the IP address, timestamp, and path
    of every incoming request.
    """

    def get_client_ip(self, request):
        """Retrieve client IP address (handles proxies)."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def process_request(self, request):
        ip = self.get_client_ip(request)
        path = request.path
        timestamp = timezone.now()

        # Save log
        RequestLog.objects.create(
            ip_address=ip,
            path=path,
            timestamp=timestamp
        )
