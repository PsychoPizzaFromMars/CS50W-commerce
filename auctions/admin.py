from django.contrib import admin
from .models import User, AuctionListing, Item_category
# Register your models here.

admin.site.register(User)
admin.site.register(AuctionListing)
admin.site.register(Item_category)