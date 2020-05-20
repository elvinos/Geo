from django.urls import path, re_path
from django.contrib import admin
from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
# from apps.drivetime.views import call_drivetime
# from rest_framework.urlpatterns import format_suffix_patterns


from config.api import api

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('logout/', logout, {'next_page': '/'}, name='logout'),
    path('api/', include(api.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += static(
            settings.STATIC_URL,
            document_root=settings.STATIC_ROOT)

    urlpatterns += static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT)

