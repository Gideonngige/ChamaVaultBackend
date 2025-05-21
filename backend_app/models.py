from django.db import models
import datetime
from django.utils.timezone import now 
from django.utils import timezone

#date validation
def validate_date(value):
    if value <= timezone.now():
        raise ValidationError("The deadline must be a future date.")
#end

#models
class Chamas(models.Model):
    chama_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.CharField(max_length=200, default="chamavault")
    description = models.TextField(max_length=500, default="This chama was created by chamavault")
    created_date = models.DateTimeField(default=now)


    def __str__(self):
        return f"{self.chama_id} - {self.name}"

class Members(models.Model):
    member_id = models.AutoField(primary_key=True)
    chama = models.ForeignKey(Chamas, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    ROLE = [
        ('member','member'),
        ('chairperson','chairperson'),
        ('treasurer','treasurer'),
        ('secretary','secretary'),
        ('admin','admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE, default='member')
    joined_date = models.DateTimeField(default=now)
    profile_image = models.URLField(default="https://i.pravatar.cc/150?img=3")
    credit_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.member_id} - {self.name}"

class MembersLocation(models.Model):
    location_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

class Contributions(models.Model):
    contribution_id = models.AutoField(primary_key=True)
    transactionRef = models.CharField(max_length=50, default="T073397058487061")
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    chama = models.ForeignKey(Chamas, on_delete=models.CASCADE, default=1)
    CONTRIBUTION_TYPE = [
        ('ordinary','ordinary'),
        ('education','education'),
    ]
    contribution_type = models.CharField(max_length=20, choices=CONTRIBUTION_TYPE, default='contribution')
    contribution_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.amount}"

class ContributionDate(models.Model):
    contribution_date_id = models.AutoField(primary_key=True)
    chama = models.ForeignKey(Chamas, on_delete=models.CASCADE, default=1)
    contribution_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.chama} - {self.contribution_date}"

class Penalty(models.Model):
    penalty_id = models.AutoField(primary_key=True)
    contribution = models.ForeignKey(Contributions, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    penalty_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.contribution} - {self.amount}"

class Defaulters(models.Model):
    defaulter_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    chama = models.ForeignKey(Chamas, on_delete=models.CASCADE, default=1)
    STATUS = [
        ('active','active'),
        ('inactive','inactive'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='active')
    def __str__(self):
        return f"{self.member} - {self.chama} - {self.status}"

class Loans(models.Model):
    loan_id = models.AutoField(primary_key=True)
    name = models.ForeignKey(Members, on_delete=models.CASCADE, related_name='loanee_name', default=5)
    chama = models.ForeignKey(Chamas, on_delete=models.CASCADE, default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    repayment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    LOAN_TYPES = [
        ('LTL', 'Long Term Loan'),
        ('STL', 'Short Term Loan'),
    ]
    LOAN_STATUS = [
        ('paid','paid'),
        ('pending','pending'),
    ]
    loan_status = models.CharField(max_length=20, choices=LOAN_STATUS, default='pending')
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES, default='LTL')
    loan_date = models.DateTimeField(auto_now_add=True)
    loan_deadline = models.DateTimeField(validators=[validate_date])

    def __str__(self):
        return f"{self.name} - {self.loan_type} - {self.amount}"

class LoanApproval(models.Model):
    loanapproval_id = models.AutoField(primary_key=True)
    loan_id = models.ForeignKey(Loans, on_delete=models.CASCADE)
    STATUS = [
        ('pending','pending'),
        ('declined','declined'),
        ('approved','approved'),
    ]
    chairperson_approval = models.CharField(max_length=45, choices=STATUS, default='pending')
    treasurer_approval = models.CharField(max_length=45, choices=STATUS, default='pending')
    secretary_approval = models.CharField(max_length=45, choices=STATUS, default='pending')


class CreditScore(models.Model):
    credit_id = models.AutoField(primary_key=True)
    member_id = models.ForeignKey(Members, on_delete=models.CASCADE)
    credit_score = models.DecimalField(max_digits=10, decimal_places=2)
    

class LoanRepayment(models.Model):
    repayment_id = models.AutoField(primary_key=True)
    loan = models.ForeignKey(Loans, on_delete=models.CASCADE, default=1, related_name="repayments")
    transactionRef = models.CharField(max_length=50, default="T073397058487061")
    chama = models.ForeignKey(Chamas, on_delete=models.CASCADE, default=1)
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    LOAN_TYPES = [
        ('LTL', 'Long Term Loan'),
        ('STL', 'Short Term Loan'),
    ]
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES, default='STL')
    penality = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chama} - {self.amount}"

class Transactions(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    transactionRef = models.CharField(max_length=50, default="T073397058487061")
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    chama = models.ForeignKey(Chamas, on_delete=models.CASCADE)
    TRANSACTION_TYPE = [
        ('Contribution','Contribution'),
        ('Loan repayment','Loan repayment'),
        ('Loan','Loan'),
        ('Expense','Expense'),
        ('Expense','Expense'),
        ('Insurance','Insurance'),
        ('Other','Other'),
    ]
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE, default='Other')
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.amount}"

class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    member_id = models.ForeignKey(Members, on_delete=models.CASCADE, null=True, blank=True)
    chama = models.ForeignKey(Chamas, on_delete=models.CASCADE, default=1)
    NOTIFICATION_TYPES = [
        ('alert', 'Alert'),
        ('event', 'Event'),
        ('emergency', 'Emergency'),
    ]
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='personal')
    notification = models.CharField(max_length=1000,default="Greetings, testing app")
    notification_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.notification_type} - {self.notification}"

class Investments(models.Model):
    chama = models.ForeignKey(Chamas, on_delete=models.CASCADE)
    investment_name = models.CharField(max_length=100, default="New Investment")  # e.g., "3-Month Project"
    description = models.TextField(default="A new Project")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 5%
    duration_months = models.IntegerField(default=0)
    image = models.URLField(default="https://via.placeholder.com/300x200.png?text=Investment+Image")
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    STATUS = [
        ('active', 'active'),
        ('inactive', 'inactive'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(default=timezone.now)

class InvestmentContribution(models.Model):
    investment = models.ForeignKey(Investments, on_delete=models.CASCADE)
    transactionRef = models.CharField(max_length=50, default="T073397058487061")
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    contributed_at = models.DateTimeField(auto_now_add=True)


class Expenses(models.Model):
    expense_id = models.AutoField(primary_key=True)
    chama = models.ForeignKey(Chamas, on_delete=models.CASCADE, default=1)
    member = models.ForeignKey(Members, on_delete=models.CASCADE, default=1)
    EXPENSES = [
        ('Rent', 'Rent'),
        ('Travel', 'Travel'),
        ('Business', 'Business'),
        ('Other', 'Other'),
    ]
    expense_type = models.CharField(max_length=20, choices=EXPENSES, default='Other')
    expense_amount =  models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    expense_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.expense_type} - {self.expense_amount}"

class Poll(models.Model):
    chama = models.ForeignKey(Chamas, on_delete=models.CASCADE, default=1)
    question = models.CharField(max_length=255)
    stop_time = models.DateTimeField()  # Store the stop time of the poll
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name="choices", on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)  # Keep track of votes for each choice

    def __str__(self):
        return self.choice_text


class MemberPoll(models.Model):
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    chama = models.ForeignKey(Chamas, on_delete=models.CASCADE, default=1)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.member} - {self.poll} - {self.choice}"


class Meeting(models.Model):
    meeting_id = models.AutoField(primary_key=True)
    chama = models.ForeignKey(Chamas, on_delete=models.CASCADE, default=1)
    agenda = models.CharField(max_length=255)
    meeting_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.agenda

class Message(models.Model):
    text = models.TextField()
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    chama = models.ForeignKey(Chamas, on_delete=models.CASCADE, default=1)
    sender = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.sender}: {self.text[:20]}"

class Insurance(models.Model):
    insurance_id = models.AutoField(primary_key=True)
    transactionRef = models.CharField(max_length=50, default="T073397058487061")
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    chama = models.ForeignKey(Chamas, on_delete=models.CASCADE, default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    insurance_date = models.DateTimeField(auto_now_add=True)