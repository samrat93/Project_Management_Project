from rest_framework import serializers
from register.models import Company


class CompanySerializer(serializers.ModelSerializer):
    """Class for company model serializers"""

    class Meta:
        model = Company
        fields = ['id', 'social_name','name','email', 'city', 'found_date']
