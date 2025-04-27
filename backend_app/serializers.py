from rest_framework import serializers
from .models import Members,Loans, Notifications, Transactions, Chamas, Contributions,Message, MemberLocation

class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = '__all__'

class MembersSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['member_id','name','joined_date']

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

class MemberLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberLocation
        fields = ['member','name', 'latitude', 'longitude', 'updated_at']
