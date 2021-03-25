from django import forms
from .models import AuctionListing
from django.core.exceptions import ValidationError

class WatchlistForm(forms.Form):
    listing = forms.ModelChoiceField(queryset=AuctionListing.objects.all())

class NewBidForm(forms.Form):
    bid_value = forms.DecimalField(max_digits=12, decimal_places=2)
    listing = forms.ModelChoiceField(queryset=AuctionListing.objects.all())
    
    def clean(self):
        cleaned_data=super().clean()
        listing = cleaned_data.get('listing')
        bid = cleaned_data.get('bid_value')
        if listing.current_price == listing.start_bid:
            if not float(listing.start_bid) <= bid:
                self._errors['bid'] = self.error_class(['Bid must be at least equal to starting price'])
        else:
            if not float(listing.current_price) < bid:
                self._errors['bid'] = self.error_class(['Bid must be greater than current price'])
        return cleaned_data



class NewCommentForm(forms.Form):
    comment_entry = forms.CharField(widget=forms.Textarea, max_length=350)
    listing = forms.ModelChoiceField(queryset=AuctionListing.objects.all())

class CloseAuctionForm(forms.Form):
    listing = forms.ModelChoiceField(queryset=AuctionListing.objects.all())