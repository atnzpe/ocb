"""
Modelo de IA para Análise de Gastos com Flet, Google Sheets e LLM.

Este projeto analisa seus gastos em uma planilha Google Sheet e 
sugere a melhor forma de pagamento para novas compras.
"""

import flet as ft
from data.data_loader import DataLoader
from data.financial_analyzer import FinancialAnalyzer
from data.decision_maker import DecisionMaker

# Informações da planilha
CREDENTIALS_PATH = "credentials.json"
SPREADSHEET_NAME = "Nome da sua Planilha"
WORKSHEET_NAME = "Nome da Aba"

# Dados financeiros do usuário 
INITIAL_BALANCE = 1500.0  
CREDIT_LIMIT = 5000.0

def carregar_dados_da_planilha():
    """Carrega os dados da planilha."""
    data_loader = DataLoader(CREDENTIALS_PATH, SPREADSHEET_NAME, WORKSHEET_NAME)
    return data_loader.load_data()

def main(page: ft.Page):
    """Função principal para executar o aplicativo Flet."""

    # Carrega os dados da planilha
    expenses_data = carregar_dados_da_planilha()

    # Cria as instâncias necessárias
    financial_analyzer = FinancialAnalyzer(expenses_data, INITIAL_BALANCE, CREDIT_LIMIT)
    decision_maker = DecisionMaker(financial_analyzer)  

    # Lógica da interface Flet (em desenvolvimento)
    page.title = "Análise de Gastos"
    page.add(ft.Text("Bem-vindo ao seu Analisador de Gastos!"))

    # ... (implementar interface para interação com o usuário) 

# Inicia o aplicativo Flet
ft.app(target=main)