# ip_tracking/views.py
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit



# Simple test view for Task 0
def test_view(request):
    return HttpResponse("IP logging middleware is working!")


# Task 3: Anonymous users → 5 requests per minute
@csrf_exempt
@ratelimit(key="ip", rate="5/m", block=True)
def anonymous_sensitive_view(request):
    return JsonResponse({"message": "Anonymous access granted"})


# Task 3: Authenticated users → 10 requests per minute
@csrf_exempt
@ratelimit(key="user_or_ip", rate="10/m", block=True)
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"status": "success", "message": "Login successful"})
        return JsonResponse({"status": "error", "message": "Invalid credentials"}, status=401)

    return HttpResponse("Login endpoint (POST only)")
