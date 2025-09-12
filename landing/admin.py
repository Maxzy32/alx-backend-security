from django.contrib import admin
from .models import Listing, Booking, Review, Payment

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "price_per_night", "is_available", "created_at")
    search_fields = ("title", "location")
    list_filter = ("is_available",)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "listing", "check_in", "check_out", "created_at")
    search_fields = ("customer_name",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("reviewer_name", "listing", "rating", "created_at")
    search_fields = ("reviewer_name", "listing__title")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "booking", "amount", "status", "created_at")
    list_filter = ("status",)

