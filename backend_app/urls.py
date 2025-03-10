from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('members/<str:email>/<str:password>/', views.members, name='members'),
    path('contributions/', views.contributions, name='contributions'),
    path('loans/<str:email>/<int:amount>/<str:loan_type>/<int:period>/', views.loans, name='loans'),
    path('loan_allowed/<str:email>/', views.loan_allowed, name='loan_allowed'),
    path('postsignIn/<str:email>/<str:password>/', views.postsignIn, name='postsignIn'),
    path('logout/', views.logout, name='logout'),
    path('postsignUp/', views.postsignUp, name='postsignUp'),
    path('postReset/<str:email>/', views.postReset, name='postReset'),
    path('createchama/', views.createchama, name='createchama'),
    path('getMember/<str:email>/', views.getMember, name='getMember'),
    path('getChama/<str:email>/', views.getChama, name='getChama'),
    path('sendEmail/<str:email_to>/<str:applink>/', views.sendEmail, name='sendEmail'),
    path('stk_push/<str:phone_number>/<int:amount>/', views.stk_push, name='stk_push'),
    path('getLoans/<str:chamaname>/<str:email>/', views.getLoans, name='getLoans'),
    path('getContributions/<str:chamaname>/<str:email>/', views.getContributions, name='getContributions'),
    path('getAllLoans/', views.getAllLoans, name='getAllLoans'),
    path('confirm_loan/<int:loanee_id>/<str:approver_email>/', views.confirm_loan, name='confirm_loan'),
    path('get_notifications/<str:email>/', views.get_notifications, name='get_notifications'),
]