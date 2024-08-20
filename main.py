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
    data_loader = DataLoader(CREDENTIALS_PATH, SPREADSHEET_NAME, WORKSHEET_NAME)
    expenses_data = data_loader.load_data()

    # Cria as instâncias necessárias
    financial_analyzer = FinancialAnalyzer(data_loader, INITIAL_BALANCE, CREDIT_LIMIT)
    decision_maker = DecisionMaker(financial_analyzer)

    # Lógica da interface Flet (em desenvolvimento)
    page.title = "Análise de Gastos"
    # Define a orientação vertical para os controles na página.
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(ft.Text("Bem-vindo ao seu Analisador de Gastos!"))
    
    # Elementos da interface
    txt_valor = ft.TextField(label="Valor da Compra")
    txt_categoria = ft.TextField(label="Categoria")
    btn_gerar_sugestao = ft.ElevatedButton("Gerar Sugestão")
    txt_sugestao = ft.Text()
    
    def gerar_sugestao_clicked(e):
        """Função chamada ao clicar no botão."""
        try:
            valor = float(txt_valor.value)
            categoria = txt_categoria.value
    
            # Obter sugestão do DecisionMaker
            sugestao = decision_maker.get_purchase_suggestion(valor, categoria)
            txt_sugestao.text = sugestao
            page.update()
        except ValueError:
            txt_sugestao.text = "Informe um valor válido."
            page.update()
    
    btn_gerar_sugestao.on_click = gerar_sugestao_clicked
    
    # Layout da página
    page.add(
        ft.Column(
            [
                txt_valor,
                txt_categoria,
                btn_gerar_sugestao,
                txt_sugestao,
            ]
        )
    )


# Inicia o aplicativo Flet
ft.app(target=main)