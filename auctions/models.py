from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    value = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

class Item_category(models.Model):
    name = models.CharField(max_length=32)    

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    desc = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listing")
    start_bid = models.DecimalField(max_digits=6, decimal_places=2)
    cur_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="current_bid")
    item_image = models.URLField()
    category = models.ForeignKey(Item_category, on_delete=models.CASCADE, related_name="categories")

class Comment(models.Model):
    entry = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_watchlist")