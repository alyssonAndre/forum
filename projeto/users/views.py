from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomLoginForm


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomLoginForm
    success_url = reverse_lazy('quizz:index')


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in.')
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self,form):
        messages.success(self.request, 'Login successful')
        return super().form_valid(form)

    def form_invalid(self,form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Registration successful')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Registration failed. Please check the information provided.')
        return super().form_invalid(form)



