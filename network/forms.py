from django import forms
from django.core.exceptions import ValidationError
from .models import User

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_pic', 'cover']

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('instance', None)
        super(EditProfileForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.current_user.pk).exists():
            raise ValidationError("Username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.current_user.pk).exists():
            raise ValidationError("Email is already in use.")
        return email
