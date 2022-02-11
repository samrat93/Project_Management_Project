import imp
from django.shortcuts import render
from rest_framework import generics
from register.models import Company
from .serializers import CompanySerializer

# Create your views here.

class CompanyApiView(generics.ListAPIView):
    """Class based view of company model"""

    queryset = Company.objects.all()
    serializer_class = CompanySerializer


