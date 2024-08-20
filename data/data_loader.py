"""Módulo responsável por carregar os dados da planilha Google Sheets."""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import List, Dict
import gspread.exceptions


class DataLoader:
    """Carrega dados de gastos de uma planilha Google Sheets."""

    def __init__(
        self, credentials_path: str, spreadsheet_name: str, worksheet_name: str
    ):
        """Inicializa o DataLoader com as informações da planilha.

        Args:
            credentials_path (str): Caminho para o arquivo JSON de credenciais do Google Cloud.
            spreadsheet_name (str): Nome da planilha Google Sheets.
            worksheet_name (str): Nome da aba da planilha.
        """
        self.credentials_path = credentials_path
        self.spreadsheet_name = spreadsheet_name
        self.worksheet_name = worksheet_name

    def load_data(self) -> List[Dict[str, str]]:
        """Carrega os dados da planilha e retorna uma lista de dicionários.

        Returns:
            List[Dict[str, str]]: Uma lista de dicionários, onde cada dicionário representa uma linha da planilha
                                e as chaves são os cabeçalhos das colunas.
                                Retorna uma lista vazia em caso de erro.
        """
        try:
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive",
            ]
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_path, scope
            )
            client = gspread.authorize(credentials)

            spreadsheet = client.open(self.spreadsheet_name)
            worksheet = spreadsheet.worksheet(self.worksheet_name)

            # Lê todos os dados da planilha, incluindo o cabeçalho
            data = worksheet.get_all_values()

            # Extrai os cabeçalhos da primeira linha
            headers = data[0]

            # Converte os dados para uma lista de dicionários
            expenses = []
            for row in data[1:]:  # Começa da segunda linha para ignorar o cabeçalho
                expense = dict(zip(headers, row))
                expense["Valor"] = float(expense["Valor"].replace(",", "."))  # Corrige a formatação do valor
                expenses.append(expense)

            print(expenses)  # Adicionei este print para ajudar na validação
            return expenses
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"Planilha '{self.spreadsheet_name}' não encontrada.")
            return []
        except FileNotFoundError:
            print(f"Arquivo de credenciais não encontrado: {self.credentials_path}")
            return []