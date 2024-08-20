# ocb/data/data_loader.py
from googleapiclient.discovery import build
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class DataLoader:
    def __init__(self, credentials_path: str, spreadsheet_name: str):
        """Inicializa o DataLoader, autentica e busca o ID da planilha."""
        self.credentials_path = credentials_path
        self.spreadsheet_name = spreadsheet_name

        # Autenticar e abrir a planilha aqui no __init__
        self.spreadsheet = self.authenticate_and_open_spreadsheet()

    def authenticate_and_open_spreadsheet(self):
        """Autentica e abre a planilha do Google Sheets."""
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        # Autenticação movida para dentro deste método
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.credentials_path, scope)
        client = gspread.authorize(credentials)
        return client.open(self.spreadsheet_name)

    def _get_spreadsheet_id(self, spreadsheet_name: str):
        """Encontra o ID da planilha pelo nome usando a API do Google Drive."""
        if not self.service:
            logging.error(
                "Falha na autenticação. Não é possível buscar a planilha.")
            return None
        try:
            drive_service = build(
                'drive', 'v3', credentials=self.service._credentials)
            results = drive_service.files().list(
                q=f"name='{
                    spreadsheet_name}' and mimeType='application/vnd.google-apps.spreadsheet'",
                fields="nextPageToken, files(id, name)"
            ).execute()
            files = results.get('files', [])

            if not files:
                logging.error(f"Planilha '{spreadsheet_name}' não encontrada.")
                return None

            if len(files) > 1:
                logging.warning(f"Múltiplas planilhas com o nome '{
                                spreadsheet_name}' encontradas. Usando a primeira.")

            spreadsheet_id = files[0]['id']
            logging.info(f"Planilha '{spreadsheet_name}' encontrada com ID: {
                         spreadsheet_id}")
            return spreadsheet_id

        except Exception as e:
            logging.error(f"Erro ao buscar ID da planilha: {e}")
            return None

    def load_data(self, worksheet_name):
        """Carrega os dados de uma aba específica da planilha."""
        try:
            worksheet = self.spreadsheet.worksheet(worksheet_name)
            data = worksheet.get_all_values()
            return data
        except gspread.exceptions.WorksheetNotFound:
            print(f"Aviso: Aba '{worksheet_name}' não encontrada na planilha.")
            return []
        except Exception as e:
            print(f"Erro ao carregar dados da planilha: {e}")
            return []

    def extrair_salario_atual(self, data):
        try:
            saldo_restante = float(data[0][4].replace(
                ',', '.'))  # Indice 4 = Saldo Restante
            logging.info(f"Saldo restante encontrado: {saldo_restante}")
            return saldo_restante
        except (IndexError, TypeError, ValueError) as e:
            logging.error(f"Erro ao acessar 'Saldo Restante': {e}")
            return 0.0

    def extrair_dividas(self, data_despesas):
        """Extrai as dívidas da aba Despesas."""
        dividas_atuais = []
        dividas_futuras = []
        # (Implementação da lógica para extrair dívidas)
        # ...
        return dividas_atuais, dividas_futuras
