from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from .serializers import MembersSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Members, Chamas, Contributions, Loans
from django.db.models import Sum

# Create your views here.
def index(request):
    now = datetime.now()
    html = f''' 
    <html>
    <body>
    <h1>Welcome to Chamavault API!</h1>
    <p>The current time is { now}.</p>
    </body>
    </html>
    '''
    return HttpResponse(html)

#start of login api
@api_view(['GET'])
def login(request, email, password):
    if request.method == 'GET':
        check_details = Members.objects.filter(email=email, password=password).values()
        if check_details:
            return Response({"message":"Login successful"})
        else:
            return Response({"message":"Invalid credentials"})

#end of login api

#start of get members api
@api_view(['GET','POST','DELETE'])
def members(request, password):
    if request.method == 'GET':
        check_password = Members.objects.filter(password=password).values()
        if check_password:
            members = Members.objects.all()
            serializer = MembersSerializer(members, many=True)
            return Response(serializer.data)
        else:
            return Response({"message":"Access denied"})
#end of get members api
        
#start of register api
@api_view(['GET'])   
def register(request, chama_id, name, email, phone_number, password):
    if request.method == 'GET':
        check_member = Members.objects.filter(email=email).values()
        if check_member:
            return Response({"message":"Email already exists"})
        else:
            chama = Chamas.objects.get(pk=chama_id)
            member = Members(chama=chama,name=name, email=email, phone_number=phone_number, password=password)
            member.save()
            return JsonResponse({"message":"Successfully registered"})
    else:
        return JsonResponse({"message":"Invalid access"})
#end of register api   

#start of contributions api
@api_view(['GET']) 
def contributions(request, email, amount):
    try:
        member = Members.objects.get(email=email)
        contribution = Contributions(member=member, amount=amount)
        contribution.save()
        return Response({"message":f"Contribution of Ksh.{amount} was successful"})
    except Members.DoesNotExist:
        return Response({"message":"Invalid email address"})

#end of contributions api

#start of loans api

#function to calculate amount of loan allowed
from decimal import Decimal
def check_loan(email):
    member = Members.objects.get(email=email)
    total_amount = Loans.objects.filter(member=member).aggregate(Sum('amount'))['amount__sum'] or 0
    loan = 0
    max_amount = 10000
    if total_amount > max_amount:
        return loan
        
    elif total_amount < max_amount:
        loan = total_amount - (Decimal('0.5') * total_amount)
        return loan

    elif total_amount == 0:
        loan = 10000
        return max_amount

@api_view(['GET'])
def loans(request, email, amount, loan_type):
    try:
        member = Members.objects.get(email=email)
        loan_deadline=timezone.now() + timedelta(days=30)
        check = check_loan(email)
        if check > 0:
            loan = Loans(member=member, amount=amount, loan_type=loan_type, loan_deadline=loan_deadline)
            loan.save()
            return Response({"message":f"Loan of Ksh.{amount} of type {loan_type} was successful"})
        else:
            return Response({"message":f"Loan of Ksh.{amount} of type {loan_type} exceeds the maximum loan limit"})
        
    except Members.DoesNotExist:
        return Response({"message":"Invalid email address"})

#end of loans api\

@api_view(['GET'])
def loan_allowed(request, email):
    max_loan = check_loan(email)
    return Response({"max_loan":f"Ksh.{max_loan}"})
