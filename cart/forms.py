from django import forms


choice=[(i,str(i)) for i in range(1,10)]
class CartAddProduct(forms.Form):
    quantity=forms.TypedChoiceField(choices=choice,coerce=int)
