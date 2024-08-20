# ocb/data/data_loader.py
from googleapiclient.discovery import build
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class DataLoader:
    def __init__(self, credentials_path: str, spreadsheet_name: str):
        """Inicializa o DataLoader, autentica e busca o ID da planilha."""
        self.service = self._authenticate(credentials_path)
        self.spreadsheet_id = self._get_spreadsheet_id(spreadsheet_name)

    def _authenticate(self, credentials_path: str):
        """Autentica na API do Google Sheets usando credenciais de conta de serviço."""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
            service = build('sheets', 'v4', credentials=credentials)
            logging.info("Autenticado com sucesso no Google Sheets!")
            return service
        except Exception as e:
            logging.error(f"Erro na autenticação: {e}")
            return None

    def _get_spreadsheet_id(self, spreadsheet_name: str):
        """Encontra o ID da planilha pelo nome."""
        if not self.service:
            logging.error(
                "Falha na autenticação. Não é possível buscar a planilha.")
            return None
        try:
            # Utiliza a API Drive para listar os arquivos do usuário
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

    def load_data(self, sheet_name: str) -> list:
        """Carrega dados de uma aba da planilha."""
        if not self.service or not self.spreadsheet_id:
            logging.error("Falha na autenticação ou planilha não encontrada.")
            return []
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id, range=sheet_name).execute()
            data = result.get('values', [])
            logging.info(
                f"Dados carregados com sucesso da planilha '{sheet_name}'")
            return data
        except Exception as e:
            logging.error(f"Erro ao carregar dados da planilha: {e}")
            return []
