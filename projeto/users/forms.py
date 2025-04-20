from django import forms
from django.contrib.auth import get_backends,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


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