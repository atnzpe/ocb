import flet as ft
from data.data_loader import DataLoader
from data.financial_analyzer import FinancialAnalyzer
from data.decision_maker import DecisionMaker


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
SPREADSHEET_NAME = "Meus Gastos OCB"
WORKSHEET_NAME = "resumo"

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

    # Elementos da interface
    page.title = "OCB - Análise de Gastos"

    txt_valor = ft.TextField(label="Valor da compra (R$)")
    txt_categoria = ft.TextField(label="Categoria da compra")
    txt_sugestao = ft.Text()

    def gerar_sugestao(e):
        """Gera a sugestão de compra e exibe na interface."""
        try:
            valor = float(txt_valor.value)
            categoria = txt_categoria.value
            sugestao = decision_maker.get_purchase_suggestion(valor, categoria)
            txt_sugestao.value = sugestao
        except ValueError:
            txt_sugestao.value = "Valor inválido. Insira um número."
        page.update()

    btn_gerar_sugestao = ft.ElevatedButton("Gerar Sugestão", on_click=gerar_sugestao)

    # Layout da página
    page.add(
        ft.Column(
            [
                ft.Text("Bem-vindo ao OCB - Seu Analisador de Gastos!"),
                txt_valor,
                txt_categoria,
                btn_gerar_sugestao,
                txt_sugestao,
            ]
        )
    )


# Inicia o aplicativo Flet
ft.app(target=main)
