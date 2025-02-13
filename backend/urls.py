
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('', include('backend_app.urls')),
    path('admin/', admin.site.urls),
]
