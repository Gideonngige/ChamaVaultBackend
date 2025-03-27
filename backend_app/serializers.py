from rest_framework import serializers
from .models import Members,Loans, Notifications, Transactions, Chamas

class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = '__all__'

class ChamasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['chama']

class LoansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loans
        fields = '__all__'

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'

class AllChamasSerializer(serializers.ModelSerializer):
    model = Chamas 
    fields = '[name]'
