from rest_framework import serializers
from .models import Members,Loans, Notifications, Transactions, Chamas, Contributions,Message

class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['name']

class ChamasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = '__all__'

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
    class Meta:
        model = Chamas 
        fields = '[name]'
    

class ContributionsSerializer(serializers.ModelSerializer):
    member = serializers.StringRelatedField()
    class Meta:
        model = Contributions
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'sender', 'timestamp']
