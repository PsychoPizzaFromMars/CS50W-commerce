from django import forms
from .models import AuctionListing
class WatchlistForm(forms.Form):
    listing = forms.ModelChoiceField(queryset=AuctionListing.objects.all())

class NewBidForm(forms.Form):
    bid_value = forms.DecimalField(max_digits=12, decimal_places=2)
    listing = forms.ModelChoiceField(queryset=AuctionListing.objects.all())

class NewCommentForm(forms.Form):
    comment_entry = forms.CharField(widget=forms.Textarea, max_length=350)
    listing = forms.ModelChoiceField(queryset=AuctionListing.objects.all())

class CloseAuctionForm(forms.Form):
    listing = forms.ModelChoiceField(queryset=AuctionListing.objects.all())