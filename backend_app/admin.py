from django.contrib import admin
from . models import Chamas, Members, Contributions, Loans, Notifications, Transactions, LoanRepayment, Investment, profit_distribution, investment_contribution, Expenses, LoanApproval, CreditScore

# Register your models here.
admin.site.register(Chamas)
admin.site.register(Members)
admin.site.register(Contributions)
admin.site.register(Loans)
admin.site.register(Notifications)
admin.site.register(Transactions)
admin.site.register(LoanRepayment)
admin.site.register(Investment)
admin.site.register(profit_distribution)
admin.site.register(investment_contribution)
admin.site.register(Expenses)
admin.site.register(LoanApproval)
admin.site.register(CreditScore)