from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', include('quizz.urls'), name='quiz'),
    path('api/', include('quizz.api_urls')),
    path('users/', include('users.urls'), name='users'),
    path('accounts/', include('allauth.urls')),
    path('', lambda request: redirect('quiz/', permanent=False)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
