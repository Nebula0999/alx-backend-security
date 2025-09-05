import datetime
from .models import RequestLog, BlockedIP
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from ipgeolocation import IpGeolocation
from django.core.cache import cache

class RequestLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

        def __call__(self, request):
            ip_address = self.get_client_ip(request)
            timestamp = datetime.datetime.now()
            path = request.path

            if BlockedIP.objects.filter(ip_address=ip_address).exists():
                return HttpResponseForbidden("Your IP has been blocked.") 
            
            cache_key = f"geo:{ip_address}"
            geo_data = cache.get(cache_key)

            if not geo_data:
                try:
                    geo_data = self.geo.lookup(ip_address)
                    cache.set(cache_key, geo_data, timeout=86400)  # Cache for 1 day
                except Exception as e:
                    geo_data = {"country": None, "city": None}

            country = geo_data.get("country", None)
            city = geo_data.get("city", None)

            RequestLog.objects.create(
                ip_address=ip_address, 
                path=path, 
                timestamp=timestamp,
                country=country,
                city=city,
            )

            return self.get_response(request)

    def process_request(self, request):
        ip = self.get_client_ip(request)
        path = request.path
        RequestLog.objects.create(ip_address=ip, path=path)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
