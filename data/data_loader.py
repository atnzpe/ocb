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

    def load_data_from_sheet(service, spreadsheet_id, sheet_range):
        """Carrega dados de um intervalo específico da planilha."""
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                    range=sheet_range).execute()
        return result.get('values', [])


def extrair_dados_resumo(service, spreadsheet_id):
    """Extrai dados da aba 'Resumo' da planilha."""
    dados_resumo = load_data_from_sheet(service, spreadsheet_id, 'Resumo!A1:G2')  # Ajustado o intervalo!

    # Criando um dicionário mais legível:
    resumo = {
        "Mes": dados_resumo[0][0],
        "Salario_Recebido": float(dados_resumo[1][1]) if dados_resumo[1][1] else 0.0,
        "Salario_a_Receber": float(dados_resumo[1][2]) if dados_resumo[1][2] else 0.0,
        "Dividas_do_Mes": float(dados_resumo[1][3]) if dados_resumo[1][3] else 0.0,
        "Dividas_Pagas": float(dados_resumo[1][4]) if dados_resumo[1][4] else 0.0,
        "Saldo_Restante": float(dados_resumo[1][5]) if dados_resumo[1][5] else 0.0,
        "Total_a_Pagar": float(dados_resumo[1][6]) if dados_resumo[1][6] else 0.0
    }
    return resumo
