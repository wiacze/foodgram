"""foodgram_backend URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from api.views.redirect import redirect_to_recipe

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('s/<str:hash_url>/', redirect_to_recipe),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
