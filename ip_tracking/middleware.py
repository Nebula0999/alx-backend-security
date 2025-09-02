import datetime
from .models import RequestLog
from django.utils.deprecation import MiddlewareMixin

class RequestLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

        def __call__(self, request):
            ip_address = self.get_client_ip(request)
            timestamp = datetime.datetime.now()
            path = request.path

            RequestLog.objects.create(
                ip_address=ip_address, 
                path=path, 
                timestamp=timestamp
            )
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