"""
OCB: Analisador de Gastos com IA - Previsão de Limites

Este aplicativo prevê seus limites de crédito e débito com base em seus dados 
de receitas e despesas, fornecendo insights financeiros personalizados.
"""

import flet as ft
from data.data_loader import DataLoader
from data.prediction_model import PredictionModel
import logging

# Configuração do Logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Informações da Planilha Google Sheets
CREDENTIALS_PATH = "credentials.json"
SPREADSHEET_NAME = "Meus Gastos OCB"
WORKSHEET_RECEITA = "receita"
WORKSHEET_DESPESA = "despesa"


def main(page: ft.Page):
    """Função principal do aplicativo."""
    page.title = "OCB - Previsão de Limites de Crédito e Débito"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Carrega os dados da planilha
    data_loader = DataLoader(CREDENTIALS_PATH, SPREADSHEET_NAME)
    receitas = data_loader.load_data(WORKSHEET_RECEITA)
    despesas = data_loader.load_data(WORKSHEET_DESPESA)

    # Verifica se os dados foram carregados
    if not receitas or not despesas:
        page.add(ft.Text("Erro ao carregar dados da planilha.", color="red"))
        return

    # Cria e treina o modelo de previsão
    modelo = PredictionModel(receitas, despesas)
    limite_credito, limite_debito = modelo.predict_limits()

    # Elementos da interface
    page.add(
        ft.Column(
            [
                ft.Text("OCB - Previsão de Limites", size=20),
                ft.Text(f"Limite de Crédito Previsto: R$ {
                        limite_credito:.2f}"),
                ft.Text(f"Limite de Débito Previsto: R$ {limite_debito:.2f}"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )


# Inicia o aplicativo Flet
ft.app(target=main)
