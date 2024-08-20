# ocb/ui/app.py
import flet as ft
from ocb.auth import authenticate_google_sheets
from ocb.data.data_loader import DataLoader
from ocb.decision_maker import DecisionMaker
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Informações da Planilha Google Sheets
CREDENTIALS_PATH = "credentials.json"
SPREADSHEET_NAME = "Minha Planilha de Gastos"
WORKSHEET_RESUMO = "resumo"

def main(page: ft.Page):
    """Função principal do aplicativo."""
    page.title = "OCB - Previsão de Limites de Crédito e Débito"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Inicializar componentes
    data_loader = DataLoader(CREDENTIALS_PATH, SPREADSHEET_NAME)
    resumo = data_loader.load_data(WORKSHEET_RESUMO)
    decision_maker = DecisionMaker()
    saldo_restante = 0.0
    limite_cartao = 1500.00  # Valor placeholder - adaptar leitura da planilha

    if resumo:
        saldo_restante = float(resumo[1][5]) if resumo[1][5] else 0.0

    # Elementos da interface
    page.add(ft.Text("OCB - Previsão de Limites", size=20))

    def on_button_click(e):
        """Processa a solicitação de compra."""
        try:
            purchase_amount = float(purchase_amount_field.value)
            if purchase_amount <= 0:
                raise ValueError("Valor da compra inválido.")
            category = category_dropdown.value
            if not category:
                raise ValueError("Selecione uma categoria.")

            suggestion = decision_maker.get_purchase_suggestion(
                saldo_restante, limite_cartao, purchase_amount, category
            )

            page.add(ft.Text(f"Sugestão: {suggestion['suggestion']}"))
            page.add(ft.Text(f"Justificativa: {suggestion['justification']}"))
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
    button = ft.ElevatedButton("Posso Comprar?", on_click=on_button_click)
    page.add(purchase_amount_field, category_dropdown, button)

if __name__ == "__main__":
    ft.app(target=main)