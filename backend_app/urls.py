from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('members/<str:password>/', views.members, name='members'),
    path('register/<int:chama_id>/<str:name>/<str:email>/<str:phone_number>/<str:password>/', views.register, name='register'),
    path('login/<str:email>/<str:password>/', views.login, name='login'),
    path('contributions/<str:email>/<int:amount>/', views.contributions, name='contributions'),
    path('loans/<str:email>/<int:amount>/<str:loan_type>/', views.loans, name='loans'),
    path('loan_allowed/<str:email>/', views.loan_allowed, name='loan_allowed'),
]