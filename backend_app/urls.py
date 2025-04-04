from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('members/<str:email>/<int:chama_id>/', views.members, name='members'),
    path('contributions/', views.contributions, name='contributions'),
    path('loans/<str:email>/<int:chama_id>/<int:amount>/<str:loan_type>/<int:period>/', views.loans, name='loans'),
    path('loan_allowed/<str:email>/', views.loan_allowed, name='loan_allowed'),
    path('postsignIn/<str:email>/<str:password>/<str:chama>/', views.postsignIn, name='postsignIn'),
    path('logout/', views.logout, name='logout'),
    path('postsignUp/', views.postsignUp, name='postsignUp'),
    path('postReset/<str:email>/', views.postReset, name='postReset'),
    path('createchama/', views.createchama, name='createchama'),
    path('getMember/<str:email>/<str:chama>/', views.getMember, name='getMember'),
    path('getChama/<str:email>/', views.getChama, name='getChama'),
    path('allchamas/', views.allchamas, name='allchamas'),
    path('sendEmail/<str:email_to>/<str:applink>/', views.sendEmail, name='sendEmail'),
    path('getLoans/<str:chamaname>/<str:email>/', views.getLoans, name='getLoans'),
    path('getContributions/<str:chamaname>/<str:email>/', views.getContributions, name='getContributions'),
    path('getAllLoans/<str:role>/', views.getAllLoans, name='getAllLoans'),
    path('confirm_loan/<int:loan_id>/<int:loanee_id>/<str:approver_email>/<str:status>/', views.confirm_loan, name='confirm_loan'),
    path('get_notifications/<str:email>/<int:chama_id>/', views.get_notifications, name='get_notifications'),
    path('transactions/<str:transaction_type>/<str:email>/<int:chama_id>/', views.transactions, name='transactions'),
    path('investment/', views.investment, name='investment'),
    path('getInvestment/<str:email>/', views.getInvestment, name='getInvestment'),
    path('calculate_investment/<int:member_id>/', views.calculate_investment, name='calculate_investment'),
]