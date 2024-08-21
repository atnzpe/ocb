# ocb/ui/app.py
import flet as ft
from auth import authenticate_google_sheets
from data.data_loader import DataLoader
from data.decision_maker import DecisionMaker
from data.financial_analyzer import FinancialAnalyzer
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Informações da Planilha Google Sheets
CREDENTIALS_PATH = "credentials.json"
SPREADSHEET_NAME = "Minha Planilha de Gastos"
WORKSHEET_RESUMO = "resumo"
WORKSHEET_DESPESAS = "despesa"

def main(page: ft.Page):
    """Função principal para iniciar o aplicativo Flet."""

    page.title = "OCB - Previsão de Limites de Crédito e Débito"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Inicializar componentes
    data_loader = DataLoader(CREDENTIALS_PATH, SPREADSHEET_NAME)
    decision_maker = DecisionMaker() #  DecisionMaker inicializado aqui

    # Elementos da interface
    page.add(ft.Text("OCB - Previsão de Limites", size=20))

    def on_button_click(e):
        """Processa a solicitação de compra quando o botão é clicado."""

        try:
            purchase_amount = float(purchase_amount_field.value)
            if purchase_amount <= 0:
                raise ValueError("Valor da compra inválido.")

            category = category_dropdown.value
            if not category:
                raise ValueError("Selecione uma categoria.")

            installments = int(installments_field.value)
            if installments <= 0:
                raise ValueError("Número de parcelas inválido.")

            payment_method = payment_method_dropdown.value
            if not payment_method:
                raise ValueError("Selecione uma forma de pagamento.")

            # Análise financeira
            financial_analyzer = FinancialAnalyzer(data_loader)
            saldo_atual = financial_analyzer.get_current_balance() 
            limite_credito = financial_analyzer.get_available_credit()  
            impacto_compra = financial_analyzer.simular_compra(
                purchase_amount, installments
            )

            # Obtém sugestão de compra
            suggestion = decision_maker.get_purchase_suggestion(
                saldo_atual, 
                limite_credito, 
                impacto_compra,
                purchase_amount, 
                installments, 
                payment_method
            )

            # Exibe a sugestão na interface

            
            page.add(ft.Text(f"Sugestão: {suggestion['suggestion']}"))
            page.add(ft.Text(f"Justificativa: {suggestion['justification']}"))
            page.add(ft.Text(f"Informação: {suggestion['resume']}"))

            page.update()

        except ValueError as e:
            page.add(ft.Text(f"Erro: {e}", color="red"))
            page.update()

    purchase_amount_field = ft.TextField(label="Valor da Compra", width=200)
    category_dropdown = ft.Dropdown(
        width=200,
        options=[
            ft.dropdown.Option("Alimentação"),
            ft.dropdown.Option("Transporte"),
            ft.dropdown.Option("Lazer"),
            # Adicione mais categorias aqui
        ],
    )
    installments_field = ft.TextField(label="Parcelas", width=100)
    payment_method_dropdown = ft.Dropdown(
        width=200,
        options=[
            ft.dropdown.Option("Cartão de Crédito"),
            ft.dropdown.Option("Cartão de Débito"),
            ft.dropdown.Option("Dinheiro"),
            # Adicione mais formas de pagamento aqui
        ],
    )
    button = ft.ElevatedButton("Posso Comprar?", on_click=on_button_click)
    
    # Adiciona os componentes na página
    page.add(
        purchase_amount_field, 
        category_dropdown,
        installments_field, 
        payment_method_dropdown, 
        button
    )

if __name__ == "__main__":
    ft.app(target=main)