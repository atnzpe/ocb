"""Módulo responsável por carregar os dados da planilha Google Sheets."""

import gspread
from oauth2client.service_account import ServiceAccountCredentials

class DataLoader:
    """Carrega dados de gastos de uma planilha Google Sheets."""

    def __init__(self, credentials_path, spreadsheet_name, worksheet_name):
        """Inicializa o DataLoader com as informações da planilha."""
        self.credentials_path = credentials_path
        self.spreadsheet_name = spreadsheet_name
        self.worksheet_name = worksheet_name

    def load_data(self):
        """Carrega os dados da planilha e retorna uma lista de dicionários."""
        # TODO: Implementar a lógica de autenticação e carregamento de dados.
        #       Utilizar gspread para acessar a API do Google Sheets.
        pass  # Remover após implementar