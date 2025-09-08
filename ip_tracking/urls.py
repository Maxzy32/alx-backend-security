from django.urls import path
from .views import test_view, anonymous_sensitive_view, login_view

urlpatterns = [
    path("test/", test_view, name="test"),
    path("anonymous/", anonymous_sensitive_view, name="anonymous"),
    path("login/", login_view, name="login"),
]
