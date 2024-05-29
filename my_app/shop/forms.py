from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item, CartItem, UserProfile



class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ItemsForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        # exclude = ['host']


class CartItemUpdateForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['country', 'first_name', 'last_name', 'address', 'city', 'state', 'postal_code', 'phone_number', 'email']


# class ShippingAddressForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = [
#             'country', 'first_name', 'last_name', 'address', 
#             'city', 'state', 'postal_code', 'phone_number', 'email'
#         ]

# class PaymentForm(forms.ModelForm):
#     class Meta:
#         model = Payment
#         fields = [
#             'method', 'card_type', 'card_number', 'card_cvv', 
#             'card_expiration_month', 'card_expiration_year'
#         ]

#         widgets = {
#             'card_expiration_month': forms.Select(choices=[(x, x) for x in range(1, 13)]),
#             'card_expiration_year': forms.Select(choices=[(x, x) for x in range(timezone.now().year, timezone.now().year + 15)])
#         }