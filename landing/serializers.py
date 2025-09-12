# landing/serializers.py
from rest_framework import serializers
from .models import Listing, Booking, Review, Payment

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "listing", "reviewer_name", "rating", "comment", "created_at"]
        read_only_fields = ["created_at"]

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "listing", "customer_name", "check_in", "check_out", "created_at"]
        read_only_fields = ["created_at"]

    def validate(self, data):
        if data["check_in"] >= data["check_out"]:
            raise serializers.ValidationError("check_out must be after check_in")

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "booking", "amount", "transaction_id", "status", "created_at"]
        read_only_fields = ["transaction_id", "created_at"]

    def create(self, validated_data):
        # Fake/simulate transaction id for demo
        import uuid
        validated_data["transaction_id"] = str(uuid.uuid4())
        payment = super().create(validated_data)
        # Optionally mark booking/listing availability, etc.
        payment.status = validated_data.get("status", "Completed")
        payment.save()
        return payment

class ListingSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Listing
        fields = ["id", "title", "description", "location", "price_per_night",
                  "is_available", "image_url", "created_at", "reviews"]
        read_only_fields = ["created_at", "reviews"]
