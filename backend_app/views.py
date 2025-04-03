from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from .serializers import MembersSerializer, ChamasSerializer, LoansSerializer, NotificationsSerializer, TransactionsSerializer, AllChamasSerializer 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Members, Chamas, Contributions, Loans, Notifications, Transactions, Investment, profit_distribution, investment_contribution, Expenses
from django.db.models import Sum
import pyrebase
import json
from django.views.decorators.csrf import csrf_exempt
from django_daraja.mpesa.core import MpesaClient
from django.core.mail import send_mail
from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth
import datetime
import base64
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Members, Chamas
import uuid
# import pyrebase4 as pyrebase

# Create your views here.
config = {
    "apiKey": "AIzaSyBYX6dcWok3ldsw4gFXHEjyKbVs6tONxKc",
    "authDomain": "chamavault-d1d35.firebaseapp.com",
    "databaseURL": "https://chamavault-d1d35-default-rtdb.firebaseio.com/",
    "projectId": "chamavault-d1d35",
    "storageBucket": "chamavault-d1d35.firebasestorage.app",
    "messagingSenderId": "739112708717",
    "appId": "1:739112708717:web:481c8338f8b5fdfb192d64",
    "measurementId": "G-47P7H86QBS"
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth() 
database = firebase.database()


def index(request):
    from datetime import datetime
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

#start of get members api
@api_view(['GET','POST','DELETE'])
def members(request, email, chama_id):
    if request.method == 'GET':
        try:
            member = Members.objects.filter(chama=chama_id,email=email)
            if member:
                members = Members.objects.filter(chama=chama_id)
                serializer = MembersSerializer(members, many=True)
                return Response(serializer.data)
            else:
                return Response({"message":"Please signin"})
        except:
            return Response({"message":"Invalid password"})
    else:
        return Response({"message":"Invalid access"})
#end of get members api  

#get member api
@api_view(['GET'])
def getMember(request, email, chama):
    try:
        chama = Chamas.objects.get(name=chama)
        member = Members.objects.get(chama=chama,email=email)
        serializer = MembersSerializer(member)
        return JsonResponse(serializer.data)
    except Members.DoesNotExist:
        return JsonResponse({"message":"Invalid email address"})
#end of get member api

#get chama api

@api_view(['GET'])
def getChama(request, email):
    try:
        # Get all Members associated with the given email
        members = Members.objects.filter(email=email)

        if not members.exists():
            return JsonResponse({"message": "No chamas found for this email"}, status=404)

        # Extract chama names instead of objects
        chamas = [member.chama.name for member in members]  # Extract only the name

        return JsonResponse({"chamas": chamas}, safe=False)

    except Exception as e:
        return JsonResponse({"message": f"Error: {str(e)}"}, status=500)

#end of get chama api


#get allchama api
@api_view(['GET'])
def allchamas(request):
    try:
        chamas = list(Chamas.objects.values('name'))  # Convert QuerySet to a list
        print(chamas)

        if not chamas:
            return JsonResponse({"message": "There is no any chama"}, status=404)

        return JsonResponse({"Chamas": chamas}, safe=False)  # Directly return JSON data

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
#end of get allchama api



#start of contributions api
# @csrf_exempt
@api_view(['POST']) 
def contributions(request):
    try:
        data = json.loads(request.body) 
        email = data.get('email')
        amount = data.get('amount')
        phonenumber = data.get('phonenumber')
        chama_id = data.get('chama_id')
        transactionRef = data.get('transactionRef')
        print(chama_id)

        member = Members.objects.filter(email=email).first()
        chama = Chamas.objects.get(name=f"Chama{chama_id}")
        print(chama)
        if member:
            contribution = Contributions(transactionRef=transactionRef, member=member, amount=amount, chama=chama)
            contribution.save()
            transaction = Transactions(transactionRef=transactionRef, member=member, amount=amount, chama=chama, transaction_type="Contribution")
            transaction.save()
            return JsonResponse({"message":f"Contribution of Ksh.{amount} to chama{chama_id} was successful","status":200})
        else:
            return JsonResponse({"message":"Please signin"})

    except Members.DoesNotExist:
        return Response({"message":"Invalid email address"})

#end of contributions api

#start of get transactions api
def transactions(request, transaction_type, email):
    member = Members.objects.filter(email=email).first()
    try:
        if not member:
            return JsonResponse({"message":"Please signin"})
        else:
            transactions = Transactions.objects.filter(member=member, transaction_type=transaction_type).order_by('-transaction_date')
            serializer = TransactionsSerializer(transactions, many=True)
            return JsonResponse(serializer.data, safe=False)
    except Members.DoesNotExist:
        return JsonResponse({"message":"Invalid email address"})

#end of get transactions api

#start of loans api

#function to calculate amount of loan allowed
from decimal import Decimal
from django.db.models import Sum

def check_loan(email):
    try:
        member = Members.objects.filter(email=email).first()
    except Members.DoesNotExist:
        return "Member not found"

    total_amount = Loans.objects.filter(name=member).aggregate(Sum('amount'))['amount__sum'] or 0
    max_amount = 10000  # Maximum loan amount
    
    if total_amount == 0:
        return max_amount  # If no loan exists, they can get the full amount
    
    elif total_amount > max_amount:
        return 500  # Fixed loan amount if they exceed max

    else:
        return float(total_amount) * 0.5  # Half of their current loan balance

#end of calculate function

@api_view(['GET'])
def loans(request, email, chama_id, amount, loan_type, period):
    try:
        member = Members.objects.filter(email=email).first()
        chama = Chamas.objects.get(name=f"Chama{chama_id}")
        print(member)
        print(chama)
        loan_deadline=timezone.now() + timedelta(days=period)
        print(loan_deadline)
        check = check_loan(email)
        print(check)
        if check == 500:
            loan = Loans(name=member, chama=chama, amount=check, loan_type=loan_type, loan_deadline=loan_deadline)
            loan.save()
            transaction = Transactions(member=member, amount=amount, chama=chama, transaction_type="Loan")
            transaction.save()
            return Response({"message":f"Loan of Ksh.{amount} of type {loan_type} was successful","status":200})

        elif check > 0:
            loan = Loans(name=member,chama=chama, amount=amount, loan_type=loan_type, loan_deadline=loan_deadline)
            loan.save()
            transaction = Transactions(member=member, amount=amount, chama=chama, transaction_type="Loan")
            transaction.save()
            return Response({"message":f"Loan of Ksh.{amount} of type {loan_type} was successful","status":200})
        else:
            return Response({"message":f"Loan of Ksh.{amount} of type {loan_type} exceeds the maximum loan limit"})
        
    except Members.DoesNotExist:
        return Response({"message":"Invalid email address"})

#end of loans api

@api_view(['GET'])
def loan_allowed(request, email):
    max_loan = check_loan(email)
    return Response({"max_loan":f"Ksh.{max_loan}"})

#start of get loans api
def getLoans(request, chamaname, email):
    try:
        member = Members.objects.filter(email=email).first()
        if member:
            chama_name = Chamas.objects.get(name=chamaname)
            total_loan = Loans.objects.filter(name=member,chama=chama_name).aggregate(total=Sum('amount'))['total'] or 0.00
            loan_date = list(Loans.objects.filter(name=member, chama=chama_name).values('loan_date'))
            return JsonResponse({"total_loan": total_loan,"loan_date":loan_date, "interest":9.5}, safe=False)

        else:
            return JsonResponse({"message":"No loans found"})
    except Members.DoesNotExist:
        return JsonResponse({"message":"Invalid email address"})
#end of getLoans api 

#start of get all loans
@api_view(['GET'])
def getAllLoans(request):
    try:
        loans = Loans.objects.all()
        serializer = LoansSerializer(loans, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Loans.DoesNotExist:
        return JsonResponse({"message":"No loans found"})
    except Exception as e:
        return JsonResponse({"error":str(e)})
#end of get all loan

#start of confirm loan api
def confirm_loan(request, loanee_id, approver_email):
    try:
        # Get the loanee
        loanee = Loans.objects.filter(name=loanee_id).first()
        if not loanee:
            return JsonResponse({"message": "Loanee not found"}, status=404)

        # Get the approver
        approver = Members.objects.filter(email=approver_email).first()
        if not approver:
            return JsonResponse({"message": "Invalid approver email"}, status=400)

        # Approve the loan
        loanee.approved_by = approver  # Assuming approved_by is a ForeignKey to Members
        loanee.save()

        new_loanee_id = Members.objects.get(member_id=loanee_id)

        # Create a notification
        notification = Notifications(
            member_id=new_loanee_id,  
            notification_type="alert",
            notification=f"Loan of Ksh.{loanee.amount} was approved by {approver_email}"
        )
        notification.save()

        return JsonResponse({"message": f"You have successfully approved KES.{loanee.amount}"})

    except Exception as e:
        return JsonResponse({"message": f"An error occurred: {str(e)}"}, status=500)
    
#end of confirm loan api

#start of get notifications api 
def get_notifications(request, email):
    try:
        member_id = Members.objects.filter(email=email).first()
        notifications = Notifications.objects.filter(member_id=member_id).order_by('notification_date')
        serializer = NotificationsSerializer(notifications, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Notifications.DoesNotExist:
        return JsonResponse({"message":"No notifications found"})
    except Exception as e:
        return JsonResponse({"error":str(e)})


#end get notifications api


#start of getSavings api
def getContributions(request, chamaname, email):
    try:
        member = Members.objects.filter(email=email).first()

        if member:
            chama_name = Chamas.objects.get(name=chamaname)
            total_contributions = Contributions.objects.filter(member=member, chama=chama_name).aggregate(total=Sum('amount'))['total'] or 0.00
            penalty = Contributions.objects.filter(member=member, chama=chama_name).aggregate(Sum('penality'))['penality__sum'] or 0.00
            saving_date = list(Contributions.objects.filter(member=member, chama=chama_name).values('contribution_date'))
            return JsonResponse({"total_contributions": total_contributions,"saving_date":saving_date, "interest":9.5, "penalty":penalty}, safe=False)

        else:
            return JsonResponse({"message":"No Contributions found"})
    except Members.DoesNotExist:
        return JsonResponse({"message":"Invalid email address"})
#end of getSavings api 

#start of investment api 
@api_view(['POST'])
def investment(request):
    try:
        data = json.loads(request.body) 
        member_id = data.get('member_id')
        chama = data.get('chama')
        contribution_amount = data.get('contribution_amount')
        investment_type = data.get('investment_type')
        investment_duration = data.get('investment_duration')

        print(f"{member_id} {chama} {contribution_amount} {investment_type} {investment_duration}")
       

        member = Members.objects.get(member_id=member_id)
        print(member)
        investmentId = Investment.objects.filter(investment_type=investment_type).first()
        investment_id = investmentId.investment_id
        print(investment_id)
        if not investment_id:
            return JsonResponse({"message":"Invalid investment type"}, status=400)
        chama = Chamas.objects.get(name=f"Chama{chama}")
        if member:
            contribution = investment_contribution(investment_id=investmentId, member_id=member, contribution_amount=contribution_amount, investment_duration=investment_duration)
            contribution.save()
            transaction = Transactions(member=member, amount=contribution_amount, chama=chama, transaction_type="Contribution")
            transaction.save()
            return JsonResponse({"message":f"Investment of Ksh.{contribution_amount} was successful","status":200})
        else:
            return JsonResponse({"message":"Please signin"})

    except Members.DoesNotExist:
        return Response({"message":"Invalid email address"})
#end of investment api

#start of get investmet 
@api_view(['GET'])
def getInvestment(request, email):
    try:
        # Get the member based on email
        member = Members.objects.filter(email=email).first()
        
        # Fetch all investment contributions and profit distributions for the member
        investment_contri = investment_contribution.objects.filter(member_id=member)
        profit_distri = profit_distribution.objects.filter(member_id=member)

        # Initialize a list to store detailed investments
        investments = []

        for contribution in investment_contri:
            # Find related profits for this specific investment
            related_profits = profit_distri.filter(investment_id=contribution.investment_id)
            total_profit_amount = sum(profit.profit_amount for profit in related_profits)

            # Append investment details to the list
            investments.append({
                "investment_type": contribution.investment_id.investment_type,
                "investment_amount": contribution.contribution_amount,
                "profit_amount": total_profit_amount,
                "investment_duration": contribution.investment_duration,
            })

        # If no investments are found for the member, return a message
        if not investments:
            return JsonResponse({"message": "No investments or profits found for this member"}, status=404)

        return JsonResponse({"investments": investments}, status=200)

    except Members.DoesNotExist:
        return JsonResponse({"message": "Member with this email does not exist"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
#end of get investment

#start of calculate investment api
@api_view(['GET'])
def calculate_investment(request, member_id):
    member = Members.objects.get(member_id=member_id)
    total_investment = investment_contribution.objects.filter(member_id=member).aggregate(total=Sum('contribution_amount'))['total'] or 0.00
    if total_investment:
        print(total_investment)
        return JsonResponse({"total": total_investment}, status=200)
    else:
        return JsonResponse({"total":0})

#end of calculate investment api



#start of signin api
def postsignIn(request, email, password, chama):
    try:
        chama = Chamas.objects.get(name=chama)
        user = authe.sign_in_with_email_and_password(email,password)
        if Members.objects.filter(chama=chama, email=email).exists() and user:
            session_id = user['idToken']
            request.session['uid'] = str(session_id)
            return JsonResponse({"message": "Successfully logged in"})
        elif not Members.objects.filter(chama=chama, email=email).exists():
            return JsonResponse({"message": f"No user found with this email found in {chama},please register"})
        elif not user:
            return JsonResponse({"message": "Invalid email"})
        else:
            return JsonResponse({"message": "please register"})
    except:
        message = "Invalid Credentials!! Please Check your data"
        return JsonResponse({"message": message})
    
    
#end of signin api

#start of logout api
def logout(request):
    try:
        del request.session['uid']
    except:
        pass 
    return JsonResponse({"message": "Successfully logged out"})
#end of logout api

#start of signUp api
@csrf_exempt
@api_view(['POST'])
def postsignUp(request):
    try:
        data = json.loads(request.body)  # Convert request body to JSON
        
        # Extract data
        email = data.get("email")  # Define email first
        chama_name = data.get("chama")
        name = data.get("name")
        phone_number = data.get("phone_number")
        password = data.get("password")

        # Check if email already exists
        chama = Chamas.objects.get(name=chama_name)
        if Members.objects.filter(email=email, chama=chama).exists():
            return JsonResponse({"message": "You already have account in this chama"}, status=400)
        # Check if chama exists
        try:
            chama = Chamas.objects.get(name=chama_name)
        except Chamas.DoesNotExist:
            return JsonResponse({"message": "Chama not found"}, status=400)
        
        member = Members.objects.get(email=email)
        if Members.objects.filter(email=email).exists():
            member = Members(chama=chama, name=name, email=email, phone_number=phone_number, password=member.password)
            member.save()
        
        else:
            # Create user
            user = authe.create_user_with_email_and_password(email, password)
            uid = user['localId']
            # Save member
            member = Members(chama=chama, name=name, email=email, phone_number=phone_number, password=uid)
            member.save()

        return JsonResponse({"message": "Successfully registered"}, status=201)

    except Exception as e:
        print("Error:", str(e))  # Log error for debugging
        return JsonResponse({"message": "Registration failed", "error": str(e)}, status=500)
#end of signUp api

#end of reset api
def postReset(request, email):
    try:
        authe.send_password_reset_email(email)
        message = "A email to reset password is successfully sent"
        return JsonResponse({"message": message})
    except:
        message = "Something went wrong, Please check the email, provided is registered or not"
        return JsonResponse({"message": message})
#start of reset api

#start of create chama api
@csrf_exempt
@api_view(['POST'])
def createchama(request):
    try:
        data = json.loads(request.body)
        chama = data.get('chama')
        description = data.get('description')
        created_by = data.get('created_by')
        if Chamas.objects.filter(name=chama).exists():
            return JsonResponse({"message": "Chama already exists"}, status=400)
        else:
            amount = 0
            chama_instance = Chamas(name=chama, amount=amount, created_by=created_by, description=description)
            chama_instance.save()
            return JsonResponse({"message": "Chama created successfully"}, status=201)
    except:
        return JsonResponse({"message": "Chama creation failed"}, status=500)
#end of create chama api


#start of send email api
def sendEmail(request, email_to, applink):
    subject = 'Invitation to ChamaVault'
    r_email = email_to
    message = f'Hi there, \n\n I would like to invite you to check out this amazing app :{applink}n\nCheers!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [r_email]
    send_mail( subject, message, email_from, recipient_list)
    return JsonResponse({"message": "ok"})

#end of send email api
