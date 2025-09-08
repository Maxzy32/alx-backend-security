# ip_tracking/tasks.py
from datetime import timedelta
from django.utils import timezone
from alx_backend_security.alx_backend_security.celery import shared_task
from .models import RequestLog, SuspiciousIP


@shared_task
def detect_anomalies():
    """Detects suspicious IPs based on request volume or sensitive paths."""
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # Get logs from the past hour
    recent_logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    # 1. Check for IPs with >100 requests/hour
    ip_counts = {}
    for log in recent_logs:
        ip_counts[log.ip_address] = ip_counts.get(log.ip_address, 0) + 1

    for ip, count in ip_counts.items():
        if count > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                reason="Excessive requests (>100/hour)"
            )

    # 2. Check for sensitive path access (/admin, /login)
    sensitive_paths = ["/admin", "/login"]
    for log in recent_logs:
        if any(log.path.startswith(path) for path in sensitive_paths):
            SuspiciousIP.objects.get_or_create(
                ip_address=log.ip_address,
                reason=f"Accessed sensitive path: {log.path}"
            )
