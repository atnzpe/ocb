import flet as ft
from data.data_loader import DataLoader
from data.prediction_model import PredictionModel
import logging

# Configuração do Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Informações da Planilha Google Sheets
CREDENTIALS_PATH = "credentials.json"
SPREADSHEET_NAME = "Minha Planilha de Gastos"
WORKSHEET_RECEITA = "receita"
WORKSHEET_DESPESA = "despesa"
WORKSHEET_RESUMO = "resumo"

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
    resumo = data_loader.load_data(WORKSHEET_RESUMO)

    # Verifica se os dados foram carregados
    if not receitas or not despesas:
        page.add(ft.Text("Erro ao carregar dados da planilha.", color="red"))
        return

    # Cria e treina o modelo de previsão
    modelo = PredictionModel(receitas, despesas,resumo)
    limite_credito, limite_debito = modelo.predict_limits()

    # Variável para armazenar o objeto de serviço autenticado
    service = None

    # Função para lidar com o clique no botão de conexão
    def connect_google_sheets(e):
        """Conecta à conta do Google Sheets."""
        nonlocal service  # Acessar a variável 'service' no escopo externo
        service = authenticate_google_sheets()
        if service:
            page.add(ft.Text("Conectado com sucesso ao Google Sheets!"))
            # Carregar os dados da planilha após autenticação
            spreadsheet_id = "YOUR_SPREADSHEET_ID"  # Substitua pelo ID da sua planilha
            data = load_data_from_sheet(service, spreadsheet_id)
            # ... (lógica para exibir os dados na interface) ...
        else:
            page.add(ft.Text("Falha ao conectar ao Google Sheets."))
        page.update()

    # Botão para conectar à conta do Google
    connect_button = ft.ElevatedButton(
        "Conectar com o Google", on_click=connect_google_sheets
    )

    # Elementos da interface
    page.add(
        connect_button,
        ft.Column(
            [
                ft.Text("OCB - Previsão de Limites", size=20),
                ft.Text(f"Limite de Crédito Previsto: R$ {limite_credito:.2f}"),
                ft.Text(f"Limite de Débito Previsto: R$ {limite_debito:.2f}"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    ft.app(target=main)