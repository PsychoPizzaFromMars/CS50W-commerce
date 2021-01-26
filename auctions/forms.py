from django import forms
from .models import AuctionListing
class WatchlistForm(forms.Form):
    listing = forms.ModelChoiceField(queryset=AuctionListing.objects.all())