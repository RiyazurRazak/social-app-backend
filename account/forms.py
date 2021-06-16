from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Account


class RegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Account

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email {email} is Already in Use")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"Username {username} is Already in Use")

    def save(self, commit=True):
        user = super().save()
        print(user)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserEditForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ('fullname', 'avatar')




