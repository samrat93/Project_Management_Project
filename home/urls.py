from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forget-password', views.forget_password_view, name='forget-password'),
    path('new-password', views.new_password_view, name='new-password'),
    path('change-password', views.change_password_view, name='change-password'),
    path('user-task', views.user_task_view, name='user-task'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)