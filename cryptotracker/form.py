import datetime

import secrets
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from cryptotracker.models import Account, UserAddress, InviteCode


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        cleaned_data = super().clean()
        name = cleaned_data["name"]

        # Length check
        if len(name) < 3 or len(name) > 20:
            raise forms.ValidationError("Invalid account name length")

        # Existence check for the same user
        if Account.objects.filter(name=name, user=self.user).exists():
            raise forms.ValidationError("You already have an account with this name")

        return name


class UserAddressForm(ModelForm):
    class Meta:
        model = UserAddress
        fields = ["public_address", "account", "wallet_type", "name"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields["account"].queryset = Account.objects.filter(user=self.user)

    def clean_public_address(self):
        cleaned_data = super().clean()
        public_address = cleaned_data["public_address"]

        # Length check
        if len(public_address) != 42:
            raise forms.ValidationError("Invalid public address length")

        # Prefix check
        if not public_address.startswith("0x"):
            raise forms.ValidationError("Invalid public address prefix")

        # Hexadecimal check
        try:
            int(public_address, 16)
        except ValueError:
            raise forms.ValidationError("Invalid public address hexadecimal")

        # Existence check
        if UserAddress.objects.filter(public_address=public_address).exists():
            raise forms.ValidationError(
                "This public address is already registered by another user."
            )

        return public_address


class EditUserAddressForm(ModelForm):
    class Meta:
        model = UserAddress
        fields = ["account", "wallet_type", "name"]


class Dateform(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
                "onchange": "this.form.submit()",
            }
        ),
        input_formats=["%Y-%m-%d"],
        label="Date",
    )

    def clean_date(self):
        date = self.cleaned_data["date"]
        if date > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the future.")
        return date


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    invite_code = forms.CharField(max_length=32, required=False, help_text="Required unless you're the first user")

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_invite_code(self):
        invite_code = self.cleaned_data.get('invite_code')
        
        # Check if this is the first user
        if User.objects.count() == 0:
            return invite_code  # First user doesn't need invite code
        
        # For subsequent users, invite code is required
        if not invite_code:
            raise forms.ValidationError("Invite code is required")
        
        # Validate invite code
        try:
            code = InviteCode.objects.get(code=invite_code, is_active=True, used_by__isnull=True)
        except InviteCode.DoesNotExist:
            raise forms.ValidationError("Invalid or already used invite code")
        
        return invite_code


class GenerateInviteCodeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def save(self, created_by):
        code = secrets.token_urlsafe(24)[:32]  # Generate random 32-char code
        return InviteCode.objects.create(
            code=code,
            created_by=created_by
        )
