from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError

class loginform(forms.Form):
    Email=forms.EmailField()
    Password=forms.CharField(widget=forms.PasswordInput)




class UserCreationForm(forms.ModelForm):
   
    password1 = forms.CharField(label="Password1", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password1", widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ["email"]

    def clean_email(self):
        email=self.cleaned_data.get("email") 
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email already registered")   
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
       class Meta:
        model = CustomUser
        fields = ["firstname","lastname","address","pincode","city","state" ]
