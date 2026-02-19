from django import forms

#from store.models import models
from .models import ShippingAddress 

class ShippingAddressForm(forms.ModelForm):
    user = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'User Name'}))
    full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}))
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    address_line1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address Line 1'}))
    address_line2 = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address Line 2 (Optional)'}))
    city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}))
    state = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State (Optional)'}))
    zipcode = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip Code (Optional)'}))
    country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}))

    class Meta:
        model = ShippingAddress
        fields = ('user', 'full_name', 'email', 'address_line1', 'address_line2', 'city', 'state', 'zipcode', 'country')

        exclude = ['user'] 