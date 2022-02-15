from unittest import TextTestRunner
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response 
from itsdangerous import Serializer
from rest_framework import generics, permissions
from register.models import Company, Invite, UserProfile
from projects.models import Project, Task
from .serializers import CompanySerializer, UserProfileSerializer, InviteSerializer, ProjectSerializer, TaskSerializer
from rest_framework import status
#from rest_framework.permissions import IsAuthenticated
from project_api import permission
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import filters
from rest_framework.settings import api_settings
from django.contrib.auth.models import User



class UserLoginApiView(ObtainAuthToken):
    """ Django login for tokan authentication """

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class CompanyApiViewSet(viewsets.ModelViewSet):
    """ Class based viewset of company model """

    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [permissions.IsAdminUser]


class UserProfileViewSet(viewsets.ModelViewSet):
    """ Hangle creating and updating user profiles """

    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permission.UpdateOwnProfile,)
    #filter_backends = (filters.SearchFilter,)
    #search_fields = ('name','email',)


class InviteApiViewSet(viewsets.ModelViewSet):
    """ View Class of Invite api serializer """

    queryset = Invite.objects.all()
    serializer_class = InviteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 


class ProjectApiViewViewSet(viewsets.ModelViewSet):
    """ View Class of Project api serializer """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAdminUser] 


class TaskApiViewSet(viewsets.ModelViewSet):
    """View Class of Task api serializer"""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAdminUser]
    



'''
class UserProfileDetailsApiView(generics.ListCreateAPIView):
    """List all the user profiles in this"""

    def get_object(self, id):
        try:
            return UserProfile.objects.get(id=id)
        except UserProfile.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, id):
        profile = self.get_object(id)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

'''