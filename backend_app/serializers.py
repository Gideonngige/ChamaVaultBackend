from rest_framework import serializers
from .models import Members,Loans, Notifications, Transactions, Chamas, Contributions,Message, MembersLocation, Defaulters, Investments, InvestmentContribution

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
    profile_image = serializers.CharField(source='member.profile_image')
    class Meta:
        model = Message
        fields = ['id', 'text', 'sender', 'timestamp', 'profile_image']

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
    
class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investments
        fields = ['id', 'investment_name', 'description', 'min_amount', 'interest_rate', 'duration_months', 'image']

class MemberInvestmentSummarySerializer(serializers.Serializer):
    investment_id = serializers.IntegerField()
    investment_name = serializers.CharField()
    total_invested = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_amount_with_profit = serializers.DecimalField(max_digits=10, decimal_places=2)

class InvestmentProfitDetailSerializer(serializers.ModelSerializer):
    investment_name = serializers.CharField(source='investment.investment_name')
    end_at = serializers.DateTimeField(source='investment.end_at')

    class Meta:
        model = InvestmentContribution
        fields = ['id', 'investment_name', 'profit', 'amount', 'end_at']

class ContributorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='member.name')
    email = serializers.EmailField(source='member.email')

    class Meta:
        model = Contributions
        fields = ['name', 'email', 'amount']