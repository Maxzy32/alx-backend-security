# ip_tracking/middleware.py
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.core.cache import cache
from ip_tracking.models import RequestLog, BlockedIP
import ipinfo   # pip install ipinfo

# 🔑 If you have a token from ipinfo.io, put it in settings.py
from django.conf import settings

class IPLoggingMiddleware(MiddlewareMixin):
    def get_client_ip(self, request):
        """Retrieve client IP (works with proxies)."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def get_geolocation(self, ip):
        """Fetch geolocation data and cache for 24h."""
        cache_key = f"geo_{ip}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        try:
            # Initialize ipinfo handler
            token = getattr(settings, "IPINFO_TOKEN", None)
            handler = ipinfo.getHandler(token) if token else ipinfo.getHandler()
            details = handler.getDetails(ip)

            data = {
                "country": details.country_name if hasattr(details, "country_name") else None,
                "city": details.city if hasattr(details, "city") else None,
            }
        except Exception:
            data = {"country": None, "city": None}

        cache.set(cache_key, data, 60 * 60 * 24)  # 24h
        return data

    def process_request(self, request):
        ip = self.get_client_ip(request)

        # 🚫 Block if IP is blacklisted
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

        # 🌍 Geolocation lookup
        geo_data = self.get_geolocation(ip)

        # ✅ Log request
        RequestLog.objects.create(
            ip_address=ip,
            path=request.path,
            timestamp=timezone.now(),
            country=geo_data.get("country"),
            city=geo_data.get("city"),
        )
