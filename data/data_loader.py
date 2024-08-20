import gspread
from typing import List, Dict
import logging

# ... (outros imports) ...

class DataLoader:
    """Carrega dados da planilha Google Sheets."""

    def __init__(self, credentials_path: str, spreadsheet_name: str):
        """Inicializa o DataLoader."""
        self.credentials_path = credentials_path
        self.spreadsheet_name = spreadsheet_name

    def _get_worksheet(self, worksheet_name: str):
        """Obtém a aba da planilha."""
        try:
            gc = gspread.service_account(filename=self.credentials_path)
            spreadsheet = gc.open(self.spreadsheet_name)
            return spreadsheet.worksheet(worksheet_name)
        except Exception as e:
            logging.error(f"Erro ao acessar planilha: {e}")
            return None

    def load_data(self, worksheet_name: str) -> List[Dict[str, str]]:
        """Carrega dados de uma aba específica da planilha."""
        try:
            worksheet = self._get_worksheet(worksheet_name)
            if worksheet:
                return worksheet.get_all_records()
            else:
                return []
        except Exception as e:
            logging.error(f"Erro ao carregar dados da planilha: {e}")
            return []

    def load_data_from_sheet(service, spreadsheet_id):
        """Carrega os dados da planilha especificada.

        Args:
            service: Objeto de serviço autorizado da API do Google Sheets.
            spreadsheet_id: ID da planilha.

        Returns:
            dict: Um dicionário contendo os dados das abas da planilha.
        """

        # Criar um dicionário para armazenar os dados de cada aba
        data = {}

        # Lista de abas a serem carregadas
        abas = ["Resumo", "Receitas", "Despesas"]

        for aba in abas:
            # Carregar os dados da aba atual
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=spreadsheet_id, 
                                    range=f'{aba}!A1:Z').execute()
            values = result.get('values', [])

            # Adicionar os dados da aba ao dicionário
            data[aba] = values

        return data