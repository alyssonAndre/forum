from django.urls import path
from .views import * 

urlpatterns = [
    path('', index, name='index'),
    path('career-test', careerTest, name='career-test'),
]
