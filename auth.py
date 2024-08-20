import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Escopos necessários para acessar a API do Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Caminho para o arquivo de credenciais da conta de serviço
CREDENTIALS_FILE = 'credentials.json'

def authenticate_google_sheets():
    """Autentica usando credenciais de conta de serviço."""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)
        return service
    except Exception as e:
        print(f"Erro na autenticação: {e}")
        return None