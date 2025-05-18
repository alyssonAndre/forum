from django import forms
from django.contrib.auth import get_backends,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import UserProfile


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email', required=True)

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username_or_email and password:
            self.user_cache = authenticate(self.request, username=username_or_email, password=password)

            if self.user_cache is None:
                try:
                    user = User.objects.get(email=username_or_email)
                    self.user_cache = authenticate(self.request, username=user.username, password=password)
                except User.DoesNotExist:
                    pass

            if self.user_cache is None:
                raise forms.ValidationError("Invalid username or email, or incorrect password.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")

            backend = self.user_cache.backend
            self.request.session['_auth_user_backend'] = backend

        return self.cleaned_data


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-0 pr-10',
                'autocomplete': 'off',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-0 pr-10',
                'autocomplete': 'off',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-0 pr-10',
                'autocomplete': 'off',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-0 pr-10',
                'autocomplete': 'off',
            }),
        }

class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('photo',)
        widgets = {
            'photo': forms.ClearableFileInput(attrs={
                'class': 'block w-full mt-1 text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50',
                'accept': 'image/*',
            }),
        }