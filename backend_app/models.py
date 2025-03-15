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
        return self.name

class Members(models.Model):
    member_id = models.AutoField(primary_key=True)
    chama = models.ForeignKey(Chamas, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    joined_date = models.DateTimeField(default=now)

    def __str__(self):
        return self.name

class Contributions(models.Model):
    contribution_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    chama = models.ForeignKey(Chamas, on_delete=models.CASCADE, default=1)
    penality = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    contribution_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.amount}"

class Loans(models.Model):
    loan_id = models.AutoField(primary_key=True)
    name = models.ForeignKey(Members, on_delete=models.CASCADE, related_name='loanee_name', default=5)
    chama = models.ForeignKey(Chamas, on_delete=models.CASCADE, default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    LOAN_TYPES = [
        ('LTL', 'Long Term Loan'),
        ('STL', 'Short Term Loan'),
    ]
    LOAN_STATUS = [
        ('paid','paid'),
        ('pending','pending'),
    ]
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES, default='LTL')
    loan_status = models.CharField(max_length=20, choices=LOAN_STATUS, default='pending')
    approved_by = models.ForeignKey(Members, on_delete=models.CASCADE, related_name='approved_by', default=4)
    loan_date = models.DateTimeField(auto_now_add=True)
    loan_deadline = models.DateTimeField(validators=[validate_date])

    def __str__(self):
        return f"{self.name} - {self.loan_type} - {self.amount}"

class LoanRepayment(models.Model):
    repayment_id = models.AutoField(primary_key=True)
    loan_id = models.ForeignKey(Loans, on_delete=models.CASCADE)
    name = models.ForeignKey(Members, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    penality = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"

class Transactions(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    chama = models.ForeignKey(Chamas, on_delete=models.CASCADE)
    TRANSACTION_TYPE = [
        ('Contribution','Contribution'),
        ('Loan repayment','Loan repayment'),
        ('Loan','Loan'),
        ('Expense','Expense'),
        ('Other','Other'),
    ]
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE, default='Other')
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.amount}"

class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    member_id = models.ForeignKey(Members, on_delete=models.CASCADE)
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

class Investment(models.Model):
    investment_id = models.AutoField(primary_key=True)
    amount_invested = models.DecimalField(max_digits=10, decimal_places=2)
    INVESTMENT_TYPES = [
        ('real estate', 'real estate'),
        ('stock', 'stock'),
    ]
    investment_type = models.CharField(max_length=20, choices=INVESTMENT_TYPES)
    STATUS = [
        ('active', 'active'),
        ('completed', 'completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS)
    investment_date = models.DateTimeField(default=now)
    def __str__(self):
        return f"{self.investment_type} - {self.amount_invested}"


class profit_distribution(models.Model):
    distribution_id = models.AutoField(primary_key=True)
    investment_id = models.ForeignKey(Investment, on_delete=models.CASCADE)
    member_id = models.ForeignKey(Members, on_delete=models.CASCADE)
    profit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.member_id} - {self.profit_amount}"

class investment_contribution(models.Model):
    contribution_id = models.AutoField(primary_key=True)
    investment_id = models.ForeignKey(Investment, on_delete=models.CASCADE)
    member_id = models.ForeignKey(Members, on_delete=models.CASCADE)
    contribution_amount = models.DecimalField(max_digits=10, decimal_places=2)
    contribution_date = models.DateTimeField(default=now)
    def __str__(self):
        return f"{self.investment_id} - {self.contribution_amount}"


class Expenses(models.Model):
    expense_id = models.AutoField(primary_key=True)
    expense_name = models.CharField(max_length=128)
    expense_amount =  models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    expense_date = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(Members, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.expense_name} - {self.expense_amount}"