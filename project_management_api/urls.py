from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', include('register.urls', namespace='register')),
    path('projects/', include('projects.urls', namespace='projects')),
    path('', include('home.urls', namespace='home')),
    path('api/', include('project_api.urls')),
]