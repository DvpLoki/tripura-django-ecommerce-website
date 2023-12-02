from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['firstname','lastname','email','mobilenumber','address','pincode','city','state','paymentmethod']

       
        
