from django import forms
from .models import Listing, ListingImage, Verification
class ListingForm(forms.ModelForm):
    images = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Listing
        fields = ['title','description','price','condition','serial_number']
class VerificationForm(forms.ModelForm):
    class Meta:
        model = Verification
        fields = ['verdict','notes','checklist']
