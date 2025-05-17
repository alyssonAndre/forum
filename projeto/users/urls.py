from django.urls import path
from .views import CustomLoginView, RegisterView, CustomLogoutView, CustomProfileView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', CustomProfileView.as_view(), name='profile'),
]