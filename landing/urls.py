from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("booking/<int:listing_id>/", views.booking, name="booking"),  # ✅
    path("booking/<int:listing_id>/create/", views.create_booking, name="create_booking"),
]
