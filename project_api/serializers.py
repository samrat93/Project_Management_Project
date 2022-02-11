from rest_framework import serializers
from register.models import Company,UserProfile, Invite
from projects.models import Project, Task
from django.contrib.auth.models import User


class CompanySerializer(serializers.ModelSerializer):
    """Class for company model serializers"""

    class Meta:
        model = Company
        fields = ['id', 'social_name','name','email', 'city', 'found_date']
        #extra_kwargs = {''}


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer class for User Profile """

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email','password']
        extra_kwargs = {
            'password':{
                'write_only':True,
                'style': {'input_type':'password'}
            }
        }

    def create(self, validated_data):
        """create and return new user"""
        user = User.objects.create_user(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user


class InviteSerializer(serializers.ModelSerializer):
    """Invite model serializer class """

    class Meta:
        model = Invite
        fields = ['inviter', 'invited']


class ProjectSerializer(serializers.ModelSerializer):
    """Project model serializer class """

    class Meta:
        model = Project
        fields = ['id', 'name', 'assign', 'efforts', 'status', 'dead_line', 'company', 'complete_per', 'description', 'add_date', 'upd_date']


class TaskSerializer(serializers.ModelSerializer):
    """Task model serializer class """

    class Meta:
        model = Task
        fields = ['id', 'project', 'assign' ,'task_name', 'status', 'due']


