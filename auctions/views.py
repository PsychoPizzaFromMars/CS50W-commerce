from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from .models import *


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == "POST":
            title = request.POST["title"]
            desc = request.POST["desc"]
            start_bid = float(request.POST["start_bid"])
            item_img_url = request.POST["item_img_url"]
            category = Item_category.objects.get(pk=request.POST["category"])
            listing = AuctionListing(title=title, desc=desc, start_bid=start_bid, item_image=item_img_url, category=category, user=user)
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            categories = Item_category.objects.order_by('name')
            return render(request, "auctions/create.html", {
                "categories": categories,
            })
    else:
        return HttpResponseRedirect(reverse("login"))

def categories(request):
    categories = Item_category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })

def listing_page(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    if listing.cur_bid:
        max_bid = AuctionListing.objects.aggregate(Max("cur_bid"))
    else:
        max_bid = None
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "max_bid": max_bid,
    })