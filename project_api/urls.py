from django.urls import path,include
from project_api import views


urlpatterns = [
    path('company/', views.CompanyApiView.as_view()),
]
