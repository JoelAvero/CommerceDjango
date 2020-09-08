from django import forms
from .models import Auction

class NewAuction(forms.Form):
    title = forms.CharField()
    desc = forms.CharField(widget=forms.Textarea)
    price = forms.IntegerField()
    category = forms.ChoiceField(choices=Auction.CATEGORIES,)
    image = forms.CharField(required=False, label="Image (url link)")


class FilterByCategories(forms.Form):
    categories = forms.ChoiceField(choices=Auction.CATEGORIES, widget=forms.RadioSelect, label="")