# backend_app/firebase_admin_init.py
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("backend_app/firebase_service_account.json")
default_app = firebase_admin.initialize_app(cred)
