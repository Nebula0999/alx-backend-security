from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import RequestLog, SuspiciousIP

SENSITIVE_PATHS = ["/admin", "/login"]


@shared_task
def detect_suspicious_ips():
    """
    Flags suspicious IPs:
    - More than 100 requests in the last hour
    - Accessing sensitive paths (/admin, /login)
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # 1. Detect high traffic IPs
    ip_counts = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values("ip_address")
        .annotate(request_count=Count("id"))
    )

    for entry in ip_counts:
        if entry["request_count"] > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=entry["ip_address"],
                reason=f"High traffic: {entry['request_count']} requests in the last hour",
            )

    # 2. Detect sensitive path access
    sensitive_logs = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=SENSITIVE_PATHS
    ).values("ip_address", "path")

    for log in sensitive_logs:
        SuspiciousIP.objects.get_or_create(
            ip_address=log["ip_address"],
            reason=f"Accessed sensitive path: {log['path']}",
        )
