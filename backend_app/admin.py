from django.contrib import admin
from . models import Chamas, Members, Contributions, Loans, Notifications, Transactions, LoanRepayment, Investments, InvestmentContribution, Expenses, LoanApproval, CreditScore, Poll, Choice, MemberPoll, Meeting, Message, MembersLocation, ContributionDate, Penalty, Defaulters, Insurance

# Register your models here.
admin.site.register(Chamas)
admin.site.register(Members)
admin.site.register(Contributions)
admin.site.register(Loans)
admin.site.register(Notifications)
admin.site.register(Transactions)
admin.site.register(LoanRepayment)
admin.site.register(Insurance)