from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField(
        "AuctionListing", blank=True, related_name="watchers")

    def __str__(self):
        return self.username


class Bid(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(
        "AuctionListing", on_delete=models.CASCADE, related_name="auction_bids"
    )
    value = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} bidded ${self.value} to {self.listing} at {self.date}"


class Item_category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    desc = models.CharField(max_length=256)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_listings")
    start_bid = models.DecimalField(max_digits=12, decimal_places=2)
    cur_bid = models.ForeignKey(
        Bid, blank=True, null=True, on_delete=models.CASCADE, related_name="current_bid")
    item_image = models.URLField(blank=True)
    category = models.ForeignKey(
        Item_category, on_delete=models.CASCADE, related_name="listings")

    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} by {self.user}"


class Comment(models.Model):
    entry = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="listing_comments")
    commenter = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="users_comments")

    def __str__(self):
        return f"{self.commenter} commented: {self.entry} at {self.date}"

