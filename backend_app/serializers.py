from rest_framework import serializers
from .models import Members,Loans, Notifications, Transactions, Chamas, Contributions,Message, MembersLocation, Defaulters

class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = '__all__'

class MembersSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['member_id','name','joined_date','profile_image']

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
        model = MembersLocation
        fields = ['location_id','member','name', 'latitude', 'longitude', 'updated_at']

class DefaultersSerializer(serializers.ModelSerializer):
    member_id = serializers.CharField(source='member.member_id')
    member_name = serializers.CharField(source='member.name')
    phone_number = serializers.CharField(source='member.phone_number')

    class Meta:
        model = Defaulters
        fields = ['member_id','member_name', 'phone_number', 'status']