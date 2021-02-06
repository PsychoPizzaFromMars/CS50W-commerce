from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from .models import *
from .forms import *


def index(request):
    listings = AuctionListing.objects.all()
    bids = Bid.objects.order_by('id', '-value')
    # if listings.cur_bid:
    #     max_bid = AuctionListing.objects.aggregate(Max("cur_bid"))
    # else:
    #     max_bid = None
    return render(request, "auctions/index.html", {
        "listings": listings,
        # "max_bid": max_bid,
    })


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
            listing = AuctionListing(title=title, desc=desc, start_bid=start_bid,
                                     item_image=item_img_url, category=category, user=user)
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
    if request.user.is_authenticated:
        user = request.user
        is_watchlisted = User.objects.filter(
            pk=user.id, watchlist=listing).exists()
    else:
        is_watchlisted = None

    if Bid.objects.filter(listing=listing).exists():
        max_bid = Bid.objects.filter(
            listing=listing).order_by("-value").first()
    else:
        max_bid = None
    # new_bid(request, user=user)
    category_id = listing.category.id
    comments = Comment.objects.filter(listing_id=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "max_bid": max_bid,
        "category_id": category_id,
        "is_watchlisted": is_watchlisted,
        "comments": comments,
    })


def category_items(request, category_id):
    listings = AuctionListing.objects.filter(
        category=Item_category.objects.get(pk=category_id))
    return render(request, "auctions/category_items.html", {
        "listings": listings,
        "category_name": Item_category.objects.get(pk=category_id)
    })


def user_watchlist_add(request):
    form = WatchlistForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        request.user.watchlist.add(form.cleaned_data['listing'])
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    raise Http404()


def user_watchlist_rm(request):
    form = WatchlistForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        request.user.watchlist.remove(form.cleaned_data['listing'])
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    raise Http404()


def new_bid(request):
    if request.user.is_authenticated:
        user = request.user
    form = NewBidForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        new_bid = Bid(value=form.cleaned_data['bid_value'],
                      listing=form.cleaned_data['listing'], user=user)
        new_bid.save()
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    raise Http404()

def watchlist_page(request):
    if request.user.is_authenticated:
        user = request.user
        watchlist = AuctionListing.objects.filter(id__in=user.watchlist.all())
        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlist
        })
    raise Http404()

def new_comment(request):
    if request.user.is_authenticated:
        user = request.user
    form = NewCommentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        new_comment = Comment(entry=form.cleaned_data['comment_entry'],
                      listing=form.cleaned_data['listing'], commenter=user)
        new_comment.save()
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    raise Http404()

def close_auction(request):
    form = CloseAuctionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        close_auction = form.cleaned_data['listing']
        close_auction.is_active = False
        close_auction.save()
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    raise Http404()