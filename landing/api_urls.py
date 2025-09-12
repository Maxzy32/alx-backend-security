# landing/urls_api.py
from rest_framework.routers import DefaultRouter
from .api_views import ListingViewSet, BookingViewSet, ReviewViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r"listings", ListingViewSet, basename="listing")
router.register(r"bookings", BookingViewSet, basename="booking")
router.register(r"reviews", ReviewViewSet, basename="review")
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = router.urls
