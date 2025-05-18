from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect,render
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomLoginForm, UserProfileForm, ProfilePhotoForm


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



class CustomLogoutView(View):

    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('index')



class CustomProfileView(LoginRequiredMixin, View):
    template_name = 'users/profile.html'
    login_url = reverse_lazy('login')

    def get(self, request):
        user_form = UserProfileForm(instance=request.user)
        profile_form = ProfilePhotoForm(instance=request.user.profile)
        return render(request, self.template_name, {
            'form': user_form,
            'profile_form': profile_form
        })

    def post(self, request):
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = ProfilePhotoForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('profile')
        else:
            messages.error(request, "Erro ao atualizar o perfil.")
            return render(request, self.template_name, {
                'form': user_form,
                'profile_form': profile_form
            })
