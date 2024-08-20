import os
import webbrowser
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


# Escopos necessários para acessar a API do Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Caminho para o arquivo de credenciais (substitua pelo seu caminho)
CREDENTIALS_FILE = 'credentials.json'

# Informações da Planilha Google Sheets
CREDENTIALS_PATH = "credentials.json"
SPREADSHEET_NAME = "Minha Planilha de Gastos"
WORKSHEET_RECEITA = "receita"
WORKSHEET_DESPESA = "despesa"
WORKSHEET_RESUMO = "resumo"

def authenticate_google_sheets():
    """Autentica o usuário com a API do Google Sheets usando OAuth 2.0.

    Retorna:
        googleapiclient.discovery.Resource: Objeto de serviço autorizado para interagir com a API do Google Sheets.
        None: Se a autenticação falhar ou o usuário negar a autorização.
    """
    creds = None
    # Verifica se o token já existe no sistema de arquivos
    if os.path.exists('token.json'):
        creds = service_account.Credentials.from_service_account_file(
            'credentials.json', scopes=SCOPES)
    # Se não houver credenciais válidas disponíveis, solicita autorização do usuário
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Salva as credenciais para o próximo uso
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    # Cria o objeto de serviço autorizado
    service = build('sheets', 'v4', credentials=creds)
    return service