from django.shortcuts import render, redirect
from django.http import HttpResponse

# Dummy listings (static version, no DB yet)
listings = [
    {
        "id": 1,
        "title": "Cozy Beachfront Cottage",
        "description": "Wake up to ocean views in this cozy beachfront getaway.",
        "price": 120,
        "location": "Cape Coast",
        "image": "img/listings/img1.jpg",
    },
    {
        "id": 2,
        "title": "Modern City Apartment",
        "description": "Stay in the heart of the city with easy access to nightlife and attractions.",
        "price": 90,
        "location": "Accra",
        "image": "img/listings/img2.jpg",
    },
    {
        "id": 3,
        "title": "Mountain View Cabin",
        "description": "Escape to nature in this rustic cabin with stunning mountain views.",
        "price": 150,
        "location": "Aburi",
        "image": "img/listings/img3.jpg",
    },
]

def home(request):
    return render(request, "landing/home.html", {"listings": listings})

def booking(request, listing_id):
    listing = next((l for l in listings if l["id"] == listing_id), None)
    return render(request, "landing/booking.html", {"listing": listing})

def create_booking(request, listing_id):
    if request.method == "POST":
        # For now, just simulate booking confirmation
        name = request.POST.get("customerName")
        return HttpResponse(f"Booking confirmed for {name} on listing {listing_id}!")
    return redirect("home")
