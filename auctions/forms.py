from django import forms
from .models import AuctionListing
class WatchlistForm(forms.Form):
    listing = forms.ModelChoiceField(queryset=AuctionListing.objects.all())

class NewBidForm(forms.Form):
    bid_value = forms.DecimalField(max_digits=12, decimal_places=2)
    listing = forms.ModelChoiceField(queryset=AuctionListing.objects.all())