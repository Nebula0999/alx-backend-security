from django.shortcuts import render
from .models import RequestLog, BlockedIP
from django_ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
@ratelimit(key='user_or_ip', rate='10/m', method="POST", block=True)
@ratelimit(key='ip', rate='5/m', method="POST", block=True)
def login_view(request):
    if request.method == 'POST':
        # Handle login logic here
        username = request.POST.get('username')
        ip_address = request.META.get('REMOTE_ADDR')
        password = request.POST.get('password')

        if username == 'admin' and password == 'password123':
            return JsonResponse({'status': 'Login successful', 'message': 'Welcome, admin!'})
            # Successful login
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)
    return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'}, status=405)
# Create your views here.
