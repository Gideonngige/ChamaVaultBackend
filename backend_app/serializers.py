from rest_framework import serializers
from .models import Members,Loans

class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = '__all__'

class ChamasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['chama']
