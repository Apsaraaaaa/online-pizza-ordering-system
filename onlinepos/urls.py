from django.contrib import admin
from django.urls import path, include  # include is needed for app URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # correctly include app URLs
]
