from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('members/<str:email>/<str:password>/', views.members, name='members'),
    path('contributions/', views.contributions, name='contributions'),
    path('loans/<str:email>/<int:amount>/<str:loan_type>/', views.loans, name='loans'),
    path('loan_allowed/<str:email>/', views.loan_allowed, name='loan_allowed'),
    path('postsignIn/<str:email>/<str:password>/', views.postsignIn, name='postsignIn'),
    path('logout/', views.logout, name='logout'),
    path('postsignUp/', views.postsignUp, name='postsignUp'),
    path('postReset/<str:email>/', views.postReset, name='postReset'),
    path('createchama/', views.createchama, name='createchama'),
    path('getMember/<str:email>/', views.getMember, name='getMember'),
    path('getChama/<str:email>/', views.getChama, name='getChama'),
]