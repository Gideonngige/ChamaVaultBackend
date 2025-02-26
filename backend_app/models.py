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
    contribution_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.amount}"

class Loans(models.Model):
    loan_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    LOAN_TYPES = [
        ('personal', 'Personal Loan'),
        ('business', 'Business Loan'),
        ('emergency', 'Emergency Loan'),
    ]
    LOAN_STATUS = [
        ('paid','paid'),
        ('pending','pending'),
    ]
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES, default='personal')
    loan_status = models.CharField(max_length=20, choices=LOAN_STATUS, default='pending')
    loan_date = models.DateTimeField(auto_now_add=True)
    loan_deadline = models.DateTimeField(validators=[validate_date])

    def __str__(self):
        return f"{self.member.name} - {self.loan_type} - {self.amount}"

class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    member_id = models.IntegerField(null=False)
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