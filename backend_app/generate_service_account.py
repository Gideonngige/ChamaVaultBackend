# generate_service_account_json.py
import json
from decouple import config

service_account_data = {
    "type": config("FIREBASE_TYPE"),
    "project_id": config("FIREBASE_PROJECT_ID"),
    "private_key_id": config("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": config("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": config("FIREBASE_CLIENT_EMAIL"),
    "client_id": config("FIREBASE_CLIENT_ID"),
    "auth_uri": config("FIREBASE_AUTH_URI"),
    "token_uri": config("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": config("FIREBASE_AUTH_PROVIDER_CERT_URL"),
    "client_x509_cert_url": config("FIREBASE_CLIENT_CERT_URL"),
    "universe_domain": config("FIREBASE_UNIVERSE_DOMAIN"),
}

with open("firebase_service_account.json", "w") as f:
    json.dump(service_account_data, f, indent=2)
