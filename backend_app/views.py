from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
# from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from .serializers import MembersSerializer, ChamasSerializer, LoansSerializer, NotificationsSerializer, TransactionsSerializer, AllChamasSerializer, ContributionsSerializer, MessageSerializer, MembersSerializer2, MemberLocationSerializer, DefaultersSerializer, InvestmentSerializer, MemberInvestmentSummarySerializer, InvestmentProfitDetailSerializer, ContributorSerializer, LoanSerializer, ChamasSerializer
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Members, Chamas, Contributions, Loans, Notifications, Transactions, Investments, InvestmentContribution, Expenses, LoanApproval, Poll, Choice, MemberPoll, Meeting, LoanRepayment, Message, MembersLocation, ContributionDate, Penalty, Defaulters, Insurance
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
import africastalking
from decimal import Decimal
from django.db.models import Sum
from datetime import date
from django.db.models import Q
import cloudinary.uploader
from . creditscore import calculate_credit_score
from decouple import config
import traceback
from django.db import models

# import backend_app.firebase_admin_init
# from firebase_admin import auth as firebase_auth
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
def members(request, chama_id):
    if request.method == 'GET':
        try:
            member = Members.objects.filter(chama=chama_id)
            if member:
                members = Members.objects.filter(chama=chama_id)
                serializer = MembersSerializer2(members, many=True)
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
        print("Chama received:", chama)

        if chama.lower() == "null":
            member = Members.objects.filter(chama=None,email=email).first()
        else:
            chama_obj = Chamas.objects.filter(name=chama).first()
            member = Members.objects.filter(chama=chama_obj, email=email).first()

        serializer = MembersSerializer(member)
        return JsonResponse(serializer.data, safe=False)

    except Members.DoesNotExist:
        return JsonResponse({"message": "Member with this email does not exist."}, status=404)

    except Chamas.DoesNotExist:
        return JsonResponse({"message": f"Chama '{chama}' not found."}, status=404)

    except Exception as e:
        return JsonResponse({"message": "Something went wrong", "error": str(e)}, status=500)

# start of count total chama members
@api_view(['GET'])
def totalchamamembers(request, chama):
    if chama.lower() == "null":
        return JsonResponse({"total_members":0})
    chama = Chamas.objects.get(name=chama)
    total_members = Members.objects.filter(chama=chama).count()
    return JsonResponse({"total_members":total_members})
# end of count total chama members

# start of total chama savings
@api_view(['GET'])
def totalchamasavings(request, chama_id):
    chama = Chamas.objects.filter(chama_id=chama_id).first()
    total_savings = Contributions.objects.filter(chama=chama).aggregate(Sum('amount'))['amount__sum'] or 0
    total_loans = Loans.objects.filter(chama=chama, loan_status="pending").aggregate(Sum('amount'))['amount__sum'] or 0
    total_loans_repaid = LoanRepayment.objects.filter(chama=chama).aggregate(Sum('amount'))['amount__sum'] or 0
    net_savings = (total_savings - total_loans) + total_loans_repaid
   
    return JsonResponse({"total_savings":net_savings})
# end of total chama savings

# start of total loans savings
@api_view(['GET'])
def totalchamaloans(request, chama_id):
    total_loans = 0
    chama = Chamas.objects.filter(chama_id=chama_id).first()
    total_loan = Loans.objects.filter(chama=chama, loan_status="pending").aggregate(Sum('amount'))['amount__sum'] or 0
    return JsonResponse({"total_loan":total_loan})
# end of total loans savings

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

# get chamas for admin
@api_view(['GET'])
def get_all_chamas(request):
    chamas = Chamas.objects.all().order_by('-created_date')  # optional: newest first
    serializer = ChamasSerializer(chamas, many=True)
    return Response(serializer.data)


#start of contributions api
# @csrf_exempt
@api_view(['POST']) 
def contributions(request):
    try:
        data = json.loads(request.body) 
        member_id = data.get('member_id')
        amount = data.get('amount')
        phonenumber = data.get('phonenumber')
        chama_id = data.get('chama_id')
        transactionRef = data.get('transactionRef')
        savingType = data.get('savingType')
        print(chama_id)

        member = Members.objects.filter(chama=chama_id, member_id=member_id).first()
        chama = Chamas.objects.get(chama_id=chama_id)
        print(chama)

        if member:
    
            contribution = Contributions(transactionRef=transactionRef, member=member, amount=amount, chama=chama, contribution_type=savingType)
            contribution.save()
            transaction = Transactions(transactionRef=transactionRef, member=member, amount=amount, chama=chama, transaction_type="Contribution")
            transaction.save()


            Notifications.objects.create(
                member_id=member,
                chama=chama,
                notification_type="alert",
                notification=f"Your contribution of KES.{amount} for {savingType} was successfully."
            )

            return JsonResponse({"message":f"Contribution of Ksh.{amount} to chama{chama_id} was successful","status":200})
            
            
        else:
            return JsonResponse({"message":"Please signin"})

    except Members.DoesNotExist:
        return Response({"message":"Invalid email address"})

#end of contributions api


#start of payloan api
# @csrf_exempt
@api_view(['POST']) 
def payloan(request):
    try:
        data = json.loads(request.body) 
        email = data.get('email')
        amount = float(data.get('amount'))  # Ensure amount is float
        loan_type = data.get('loan_type')
        phonenumber = data.get('phonenumber')
        chama_id = data.get('chama_id')
        transactionRef = data.get('transactionRef')
        loan_id = data.get("loanId")

        print(f"Chama ID: {chama_id}")
        print(f"Loan ID: {loan_id}")
        
        chama = Chamas.objects.get(chama_id=chama_id)
        member = Members.objects.filter(chama=chama, email=email).first()
        loan = Loans.objects.get(loan_id=loan_id)

        if member:
            # Save the new repayment
            repayment = LoanRepayment(
                loan=loan,
                transactionRef=transactionRef,
                chama=chama,
                member=member,
                amount=amount,
                loan_type=loan_type
            )
            repayment.save()

            # Save transaction
            transaction = Transactions(
                transactionRef=transactionRef,
                member=member,
                amount=amount,
                chama=chama,
                transaction_type="Loan repayment"
            )
            transaction.save()

            # Calculate total repayments for the loan
            total_repaid = LoanRepayment.objects.filter(loan=loan).aggregate(total=Sum('amount'))['total'] or 0.0

            print(f"Total repaid so far: {total_repaid}, Loan amount: {loan.repayment_amount}")

            # If total repayments equal or exceed loan amount, mark as paid
            if round(total_repaid,2) >= round(loan.repayment_amount,2):
                loan.loan_status = 'paid'  # Make sure your model uses 'paid' as the correct status
                loan.save()

            return JsonResponse({
                "message": f"Loan repayment of Ksh.{amount} to chama {chama_id} was successful",
                "status": 200
            })
        else:
            return JsonResponse({"message": "Please sign in"}, status=401)

    except Chamas.DoesNotExist:
        return JsonResponse({"message": "Chama not found"}, status=404)
    except Loans.DoesNotExist:
        return JsonResponse({"message": "Loan not found"}, status=404)
    except Members.DoesNotExist:
        return JsonResponse({"message": "Member not found"}, status=404)
    except Exception as e:
        print("An unexpected error occurred:")
        traceback.print_exc()  # This shows the exact line and cause
        return JsonResponse({
        "message": f"Internal server error: {str(e)}",
        "traceback": traceback.format_exc()
         }, status=500)


#end of payloan api


#start of get transactions api
def transactions(request, transaction_type, email, chama_id):
    member = Members.objects.filter(email=email, chama=chama_id).first()
    try:
        if not member:
            return JsonResponse({"message":"Please signin"})
        else:
            if transaction_type == "Loan":
                transactions = Transactions.objects.filter(member=member, chama=chama_id, transaction_type__in=[transaction_type, "Loan repayment"]).order_by('-transaction_date')
            elif transaction_type == "Contribution":
                transactions = Transactions.objects.filter(member=member, chama=chama_id, transaction_type__in=[transaction_type]).order_by('-transaction_date')
            
            serializer = TransactionsSerializer(transactions, many=True)
            return JsonResponse(serializer.data, safe=False)
    except Members.DoesNotExist:
        return JsonResponse({"message":"Invalid email address"})

#end of get transactions api

#start of loans api

#function to calculate amount of loan allowed

def calc_repayment_amount(amount, months, loan_type):
    if loan_type == "LTL":
        interest = amount * 0.01 * months / 12
        repayment_amount =amount +  interest
        return repayment_amount
    elif loan_type == "STL":
        interest = amount * 0.1 * months / 12
        repayment_amount = amount + interest
        return repayment_amount
   
#end of calculate function


# africastalking.initialize(username='sandbox', api_key='atsk_35b2da862cc85124c522aec60fa8eedde173fc50f9fb9e0645ca97e6252f2c535930259b')
# sms = africastalking.SMS
@api_view(['GET'])
def loans(request, member_id, chama_id, amount, loan_type):
    try:
        print(chama_id)
        chama = Chamas.objects.get(chama_id=chama_id)
        member = Members.objects.filter(chama=chama,member_id=member_id).first()
        total_savings = Contributions.objects.filter(chama=chama).aggregate(Sum('amount'))['amount__sum'] or 0
        total_loans = Loans.objects.filter(chama=chama, loan_status="pending").aggregate(Sum('amount'))['amount__sum'] or 0
        total_loans_repaid = LoanRepayment.objects.filter(chama=chama).aggregate(Sum('amount'))['amount__sum'] or 0
        net_savings = (total_savings - total_loans) + total_loans_repaid
        if amount > net_savings:
            return Response({"message":"chama has insufficient funds","status":200})
        
        period = 0
        if loan_type == "LTL":
            period = 360
        elif loan_type == "STL":
            period = 90

        loan_deadline=timezone.now() + timedelta(days=period)
        print(loan_deadline)

        months = period / 30
        repayment_amount = calc_repayment_amount(amount, months, loan_type)
        if loan_type == "LTL":
            loan = Loans(name=member, chama=chama, amount=amount, repayment_amount=repayment_amount, loan_status="pending", loan_type=loan_type, loan_deadline=loan_deadline)
            loan.save()
            transaction = Transactions(member=member, amount=amount, chama=chama, transaction_type="Loan")
            transaction.save()

            Notifications.objects.create(
                member_id=member,
                chama=chama,
                notification_type="alert",
                notification=f"Your loan request of KES.{amount} has been granted successfully"
            )

            return Response({"message":f"Loan of Ksh.{amount} of type {loan_type} was successfully.","status":200})

        elif loan_type == "STL":
            loan = Loans(name=member,chama=chama, amount=amount, repayment_amount=repayment_amount, loan_status="pending", loan_type=loan_type, loan_deadline=loan_deadline)
            loan.save()
            transaction = Transactions(member=member, amount=amount, chama=chama, transaction_type="Loan")
            transaction.save()

            # response = sms.send("Hello", ["07123456789"], sender_id="Chamavault")
            # response = sms.send("Hello", ["+254797655727"])
            # print(response)
            Notifications.objects.create(
                member_id=member,
                chama=chama,
                notification_type="alert",
                notification=f"Your short terms loan of KES.{amount} has been granted successfully"
            )

            return Response({"message":f"Loan of Ksh.{amount} of type {loan_type} was successful","status":200})
        else:
            return Response({"message":f"Loan of Ksh.{amount} of type {loan_type} was not successful","status":400})
        
    except Members.DoesNotExist:
        return Response({"message":"Invalid email address"})

#end of loans api


#start of get loans api

def getLoans(request, chama_id, email):
    try:
        chama = Chamas.objects.filter(chama_id=chama_id).first()
        if not chama:
            return JsonResponse({"message": "Chama not found"}, status=404)

        member = Members.objects.filter(chama=chama, email=email).first()
        if not member:
            return JsonResponse({"message": "Member not found"}, status=404)

        if not Loans.objects.filter(name=member, chama=chama).exists():
            return JsonResponse({"message": "No loans found for this member"}, status=404)

        pending_loan = Loans.objects.filter(name=member, chama=chama, loan_status="pending").first()
        if not pending_loan:
            return JsonResponse({"message": "No pending loan found"}, status=404)

        # Short Term Loan Summary
        stl_loan = Loans.objects.filter(name=member, chama=chama, loan_status="pending", loan_type="STL").first()
        ltl_loan = Loans.objects.filter(name=member, chama=chama, loan_status="pending", loan_type="LTL").first()
        if not stl_loan:
            stl_id = 0
        else:
            stl_id = stl_loan.loan_id if stl_loan else 0
        
        if not ltl_loan:
            ltl_id = 0
        else:
            ltl_id = ltl_loan.loan_id if ltl_loan else 0



        total_stl_loan = float(Loans.objects.filter(name=member, chama=chama, loan_status="pending", loan_type="STL").aggregate(total=Sum('amount'))['total'] or 0.00)
        total_stl_repayment = float(Loans.objects.filter(name=member, chama=chama, loan_status="pending", loan_type="STL").aggregate(total=Sum('repayment_amount'))['total'] or 0.00)
        stl_loan_date = list(Loans.objects.filter(name=member, chama=chama, loan_type="STL").values('loan_date'))
        stl_loan_deadline = list(Loans.objects.filter(name=member, chama=chama, loan_type="STL").values('loan_deadline'))

        total_loan = total_stl_loan

        total_ltl_loan = float(Loans.objects.filter(name=member, chama=chama, loan_status="pending", loan_type="LTL").aggregate(total=Sum('amount'))['total'] or 0.00)
       
        total_ltl_repayment = float(Loans.objects.filter(name=member, chama=chama, loan_status="pending", loan_type="LTL").aggregate(total=Sum('repayment_amount'))['total'] or 0.00)
        ltl_loan_date = list(Loans.objects.filter(name=member, chama=chama, loan_type="LTL").values('loan_date'))
        ltl_loan_deadline = list(Loans.objects.filter(name=member, chama=chama, loan_type="LTL").values('loan_deadline'))

        total_loan += total_ltl_loan

        return JsonResponse({
            "total_loan": total_loan,
            "stl_id":stl_id,
            "total_stl_loan": total_stl_loan,
            "total_ltl_loan": total_ltl_loan,
            "ltl_id":ltl_id,
            "total_stl_repayment": total_stl_repayment,
            "total_ltl_repayment": total_ltl_repayment,
            "stl_loan_date": stl_loan_date,
            "stl_loan_deadline": stl_loan_deadline,
            "ltl_loan_date": ltl_loan_date,
            "ltl_loan_deadline": ltl_loan_deadline,
        }, safe=False)
     

    except Exception as e:
        return JsonResponse({"message": f"Server error: {str(e)}"}, status=500)


#end of getLoans api 

# get loan repayment for specific member

def getloanrepayment(request, chamaname, member_id):
    try:
        chama = Chamas.objects.get(name=chamaname)
        member = Members.objects.filter(member_id=member_id, chama=chama).first()

        if not member:
            return JsonResponse({"message": "Member not found"}, status=404)

        # STL Loans (all pending)
        stl_loans = Loans.objects.filter(name=member, chama=chama, loan_type="STL", loan_status="pending")
        print(stl_loans)
        total_stl_repaid = LoanRepayment.objects.filter(
        loan__in=stl_loans,member=member, chama=chama, loan_type="STL"
        ).aggregate(total=Sum('amount'))['total'] or 0.00
        print(total_stl_repaid)

        # LTL Loans (all pending)
        ltl_loans = Loans.objects.filter(name=member, chama=chama, loan_type="LTL", loan_status="pending")
        total_ltl_repaid = LoanRepayment.objects.filter(
            loan__in=ltl_loans, member=member, chama=chama, loan_type="LTL"
        ).aggregate(total=Sum('amount'))['total'] or 0.00

        return JsonResponse({
            "STL": {
                "repaid_amount": float(total_stl_repaid),
            },
            "LTL": {
                "repaid_amount": float(total_ltl_repaid),
            }
        }, status=200)

    except Chamas.DoesNotExist:
        return JsonResponse({"message": "Chama not found"}, status=404)
    except Exception as e:
        return JsonResponse({"message": f"Server error: {str(e)}"}, status=500)



# end of get loan repayment for specific member

#start of get all loans
@api_view(['GET'])
def getAllLoans(request, role, chama_id):
    try:
        chama = Chamas.objects.get(chama_id=chama_id)
        if role == "chairperson":
            loans = LoanApproval.objects.filter(chairperson_approval="pending")
            loan_ids = loans.values_list('loan_id', flat=True)
            print(list(loan_ids))  
            loans = Loans.objects.filter(chama=chama,loan_id__in=loan_ids, loan_type="LTL")
            serializer = LoansSerializer(loans, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif role == "treasurer":
            loans = LoanApproval.objects.filter(treasurer_approval="pending")
            loan_ids = loans.values_list('loan_id', flat=True)
            print(list(loan_ids))  
            loans = Loans.objects.filter(chama=chama,loan_id__in=loan_ids)
            serializer = LoansSerializer(loans, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif role == "secretary":
            loans = LoanApproval.objects.filter(secretary_approval="pending")
            loan_ids = loans.values_list('loan_id', flat=True)
            print(list(loan_ids))  
            loans = Loans.objects.filter(chama=chama,loan_id__in=loan_ids)
            serializer = LoansSerializer(loans, many=True)
            return JsonResponse(serializer.data, safe=False)
        
    except Loans.DoesNotExist:
        return JsonResponse({"message":"No loans found"})
    except Exception as e:
        return JsonResponse({"error":str(e)})
#end of get all loan


#start of get notifications api 
def get_notifications(request, email, chama_id):
    try:
        member_id = Members.objects.filter(email=email, chama=chama_id).first()
        notifications = Notifications.objects.filter(Q(chama=chama_id),
        Q(member_id=member_id) | Q(member_id__isnull=True)).order_by('-notification_date')
        serializer = NotificationsSerializer(notifications, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Notifications.DoesNotExist:
        return JsonResponse({"message":"No notifications found"})
    except Exception as e:
        return JsonResponse({"error":str(e)})
#end get notifications api


#start of getSavings api
def getContributions(request, chama_id, member_id):
    try:
        member = Members.objects.filter(member_id=member_id, chama=chama_id).first()
        contributions = Contributions.objects.filter(chama=chama_id, member=member).first()

        if member:
            chama = Chamas.objects.get(chama_id=chama_id)
            total_edu_contributions = Contributions.objects.filter(member=member, chama=chama_id, contribution_type="education").aggregate(total=Sum('amount'))['total'] or 0.00
            total_ord_contributions = Contributions.objects.filter(member=member, chama=chama_id, contribution_type="ordinary").aggregate(total=Sum('amount'))['total'] or 0.00
            
            return JsonResponse({"total_edu_contributions": total_edu_contributions,"total_ord_contributions":total_ord_contributions}, safe=False)

        else:
            return JsonResponse({"message":"No Contributions found"})
    except Members.DoesNotExist:
        return JsonResponse({"message":"Invalid email address"})
#end of getSavings api 


#start of signin api
def postsignIn(request, email, password, chama=None):
    try:

        # Authenticate user via Firebase
        user = authe.sign_in_with_email_and_password(email, password)
        session_id = user['idToken']
        request.session['uid'] = str(session_id)

        # Handle case where chama is not provided or is "null"
        if not chama or chama.lower() == "null":
            if Members.objects.filter(email=email).exists():
                print("Yes")
                return JsonResponse({
                    "message": "Successfully logged in",
                    "has_chama": False
                })
            else:
                return JsonResponse({
                    "message": "Account found in Firebase, but not in the database. Please register.",
                }, status=404)

        # If chama is provided, validate it
        try:
            chama_obj = Chamas.objects.get(name=chama)
        except Chamas.DoesNotExist:
            return JsonResponse({"message": f"Chama '{chama}' does not exist"}, status=404)

        if Members.objects.filter(chama=chama_obj, email=email).exists():
            return JsonResponse({
                "message": "Successfully logged in",
                "has_chama": True
            })
        else:
            return JsonResponse({
                "message": f"No user found in chama '{chama}' with this email.",
            }, status=404)

    except Exception as e:
        print("Login error:", str(e))
        return JsonResponse({
            "message": "Invalid credentials. Please check your email and password.",
            "error": str(e)
        }, status=400)

    
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
@parser_classes([MultiPartParser, FormParser])
def postsignUp(request):
    try:
        email = request.data.get("email")
        name = request.data.get("name")
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")
        profile_image = request.FILES.get("profile_image")

        # Check if email already exists
        if Members.objects.filter(email=email).exists():
            return JsonResponse({"message": "An account with this email already exists"}, status=400)

        # Upload image to Cloudinary if provided
        image_url = None
        if profile_image:
            upload_result = cloudinary.uploader.upload(profile_image)
            image_url = upload_result.get("secure_url")

        # Create Firebase user
        user = authe.create_user_with_email_and_password(email, password)
        uid = user['localId']

        # Save Member
        member = Members(
            chama=None,
            name=name,
            email=email,
            phone_number=phone_number,
            password=uid,
            role="member",
            profile_image=image_url  # Ensure your model has this field
        )
        member.save()

        return JsonResponse({"message": "Successfully registered"}, status=201)

    except Exception as e:
        print("Error:", str(e))
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


#get members contribution
def getmemberscontribution(request, chama_id):
    try:
        contributions = Contributions.objects.filter(chama=chama_id).order_by('-contribution_date')
        serializer = ContributionsSerializer(contributions, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Members.DoesNotExist:
        return JsonResponse({"message":"Invalid email address"})
# end of get memebr contrinution


# start of joinchama api
@csrf_exempt
@api_view(['GET'])
def joinchama(request, member_id, chama_name):
    try:
        member = Members.objects.get(member_id=member_id)
    except Members.DoesNotExist:
        return JsonResponse({"message": "Member not found"}, status=404)

    try:
        chama = Chamas.objects.get(name=chama_name)
    except Chamas.DoesNotExist:
        return JsonResponse({"message": "Chama not registered"}, status=404)

    # Check if member has no chama assigned
    if member.chama is None:
        member.chama = chama
        member.save()
        return JsonResponse({"message": f"You have successfully joined {chama_name}"})

    # Check if the same member has not already joined this chama with a different record
    elif not Members.objects.filter(phone_number=member.phone_number, chama=chama).exists():
        new_member = Members(
            chama=chama,
            name=member.name,
            email=member.email,
            phone_number=member.phone_number,
            password=member.password,
            role="member",
            profile_image = member.profile_image
        )
        new_member.save()
        return JsonResponse({"message": f"You have successfully joined {chama_name}"})

    else:
        return JsonResponse({"message": "You already have an account in this chama"})
# end of joinchama api

# start of update profile api
@csrf_exempt
@api_view(['POST'])
@parser_classes([MultiPartParser])
def updateprofile(request):
    try:
        member_id = request.data.get('member_id')
        name = request.data.get('name')
        phone_number = request.data.get('phone_number')
        profile_image = request.FILES.get('profile_image', None)

        member = Members.objects.get(member_id=member_id)

        if name:
            member.name = name
        if phone_number:
            member.phone_number = phone_number
        
        image_url = None
        if profile_image:
            upload_result = cloudinary.uploader.upload(profile_image)
            image_url = upload_result.get("secure_url")
            member.profile_image = image_url  # Assuming this is an ImageField

        member.save()
        return JsonResponse({"message": "ok"})

    except Members.DoesNotExist:
        return JsonResponse({"message": "Member not found"}, status=404)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

# end of update profile api

# start of function to change roles
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Members, Chamas  # Adjust the import based on your project structure

def changeroles(request, chama_id, chairperson_id, treasurer_id, secretary_id):
    chama = get_object_or_404(Chamas, chama_id=chama_id)

    # CHAIRPERSON
    if chairperson_id != 0:
        try:
            new_member = Members.objects.get(chama=chama, member_id=chairperson_id)
            old_member = Members.objects.filter(chama=chama, role="chairperson").first()
            if old_member:
                old_member.role = "member"
                old_member.save()
            new_member.role = "chairperson"
            new_member.save()
        except Members.DoesNotExist:
            return JsonResponse({"error": "Chairperson member not found"}, status=404)

    # TREASURER
    if treasurer_id != 0:
        try:
            new_member = Members.objects.get(chama=chama, member_id=treasurer_id)
            old_member = Members.objects.filter(chama=chama, role="treasurer").first()
            if old_member:
                old_member.role = "member"
                old_member.save()
            new_member.role = "treasurer"
            new_member.save()
        except Members.DoesNotExist:
            return JsonResponse({"error": "Treasurer member not found"}, status=404)

    # SECRETARY
    if secretary_id != 0:
        try:
            new_member = Members.objects.get(chama=chama, member_id=secretary_id)
            old_member = Members.objects.filter(chama=chama, role="secretary").first()
            if old_member:
                old_member.role = "member"
                old_member.save()
            new_member.role = "secretary"
            new_member.save()
        except Members.DoesNotExist:
            return JsonResponse({"error": "Secretary member not found"}, status=404)

    return JsonResponse({"message": "Roles updated successfully"}, status=200)

# end of function to change roles


# transfer money to members using paystack
def send_mpesa_payout(request, phone_number, name, amount_kes, reason="Payout"):
    # phone_number = "0710000000"
    PAYSTACK_SECRET_KEY = "sk_test_adb8f6fbc4bab87dc6814514ab1d7b9df87faea4"

    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    # Step 1: Create transfer recipient
    recipient_payload = {
        "type": "mobile_money",
        "name": name,
        "account_number": phone_number,
        "bank_code": "MPESA",  # M-Pesa code in Paystack
        "currency": "KES"
    }

    recipient_res = requests.post("https://api.paystack.co/transferrecipient", json=recipient_payload, headers=headers)
    recipient_data = recipient_res.json()

    if not recipient_data.get("status"):
        return JsonResponse({
            "success": False,
            "stage": "create_recipient",
            "error": recipient_data.get("message", "Failed to create recipient")
        }, status=400)

    recipient_code = recipient_data["data"]["recipient_code"]

    # Step 2: Make the transfer
    transfer_payload = {
        "source": "balance",
        "amount": int(float(amount_kes) * 100),  # Convert to kobo
        "recipient": recipient_code,
        "reason": reason
    }

    transfer_res = requests.post("https://api.paystack.co/transfer", json=transfer_payload, headers=headers)
    transfer_data = transfer_res.json()

    if not transfer_data.get("status"):
        return JsonResponse({
            "success": False,
            "stage": "transfer",
            "error": transfer_data.get("message", "Failed to initiate transfer")
        }, status=400)

    return JsonResponse({
        "success": True,
        "message": "Transfer successful",
        "transfer": transfer_data["data"]
    })


# insurance api
@api_view(['POST']) 
def insurance(request):
    try:
        data = json.loads(request.body) 
        email = data.get('email')
        amount = data.get('amount')
        phonenumber = data.get('phonenumber')
        chama_id = data.get('chama_id')
        transactionRef = data.get('transactionRef')
        
        chama = Chamas.objects.get(chama_id=chama_id)
        member = Members.objects.filter(chama=chama, email=email).first()

        insurance_save = Insurance(transactionRef=transactionRef, member=member, amount=amount, chama=chama)
        insurance_save.save()
        transaction = Transactions(transactionRef=transactionRef, member=member, amount=amount, chama=chama, transaction_type="Insurance")
        transaction.save()
        Notifications.objects.create(
            member_id=member,
            chama=chama,
            notification_type="alert",
            notification=f"Your insurance of KES.{amount} was successfully"
        )
        return Response({"message":"Insurance deposited successfully"})


    except Members.DoesNotExist:
        return Response({"message":"Invalid email address"})

# end of insurance api
@api_view(['GET']) 
def get_total_insurance(request, member_id, chama_id):
    try:
        chama = Chamas.objects.filter(chama_id=chama_id).first()
        member = Members.objects.filter(chama=chama, member_id=member_id).first()

        total_insurance = Insurance.objects.filter(chama=chama, member_id=member).aggregate(Sum('amount'))['amount__sum'] or 0
        return Response({"total_insurance":total_insurance})
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)