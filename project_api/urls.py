from django.urls import path,include
from rest_framework.routers import DefaultRouter
from project_api import views


router = DefaultRouter()
router.register('profile', views.UserProfileViewSet)
router.register('company',viewset=views.CompanyApiViewSet)
router.register('project',views.ProjectApiViewViewSet)
router.register('task',views.TaskApiViewSet)
router.register('invite',views.InviteApiViewSet)


urlpatterns = [
    #path('company/', views.CompanyApiView.as_view()),
    #path('user-profile', views.UserProfileApiView.as_view()),
    #path('user-profile/<int:id>', views.UserProfileDetailsApiView.as_view()),
    # path('invite', views.InviteApiView.as_view()),
    # path('project', views.ProjectApiView.as_view()),
    # path('task', views.TaskApiView.as_view()),
    #path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('login/', views.UserLoginApiView.as_view())
]
