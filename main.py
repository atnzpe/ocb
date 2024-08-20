"""
OCB: Analisador de Gastos com IA - Um projeto para auxiliar na tomada de decisão financeira.

Este projeto analisa seus gastos em uma planilha Google Sheet, gera sugestões personalizadas
utilizando um modelo de linguagem (GPT-2) e análise de sentimento, e apresenta os resultados
em uma interface gráfica interativa com gráficos.
"""

import flet as ft
from data.data_loader import DataLoader
from data.financial_analyzer import FinancialAnalyzer
from data.decision_maker import DecisionMaker
import logging
from flet.matplotlib_chart import MatplotlibChart #para grafico
import matplotlib.pyplot as plt #para grafico

# Configuração do Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Informações da Planilha Google Sheets
CREDENTIALS_PATH = "credentials.json" 
SPREADSHEET_NAME = "Meus Gastos OCB" 
WORKSHEET_NAME = "resumo"  

# Dados Financeiros do Usuário
INITIAL_BALANCE = 1500.0  
CREDIT_LIMIT = 5000.0  

def carregar_dados_da_planilha():
    """Carrega os dados da planilha, com tratamento de erros."""
    try:
        data_loader = DataLoader(CREDENTIALS_PATH, SPREADSHEET_NAME, WORKSHEET_NAME)
        return data_loader.load_data()
    except Exception as e:
        logging.error(f"Erro ao carregar dados da planilha: {e}")
        return [] 

def main(page: ft.Page):
    """Função principal que executa o aplicativo Flet."""
    page.title = "OCB - Análise de Gastos com IA"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START #ajuste para o grafico

    expenses_data = carregar_dados_da_planilha()
    if not expenses_data:
        page.add(ft.Text("Erro ao carregar dados da planilha.", color="red"))
        return

    financial_analyzer = FinancialAnalyzer(expenses_data, INITIAL_BALANCE, CREDIT_LIMIT)
    decision_maker = DecisionMaker(financial_analyzer)

    # Interface do Usuário
    txt_valor = ft.TextField(label="Valor da compra (R$)")
    txt_categoria = ft.TextField(label="Categoria da compra")
    txt_sugestao = ft.Text()
    progress_indicator = ft.ProgressRing(visible=False) 
    error_message = ft.Text(color="red", size=12)

    def gerar_sugestao(e):
        """Gera a sugestão de compra com feedback visual e logging."""
        error_message.value = ""  
        txt_sugestao.value = "" 

        try:
            logging.info("Iniciando a análise da compra.")
            progress_indicator.visible = True  
            page.update()

            valor = float(txt_valor.value)
            categoria = txt_categoria.value
            sugestao = decision_maker.get_purchase_suggestion(valor, categoria)
            txt_sugestao.value = sugestao["suggestion"]
            logging.info(f"Sugestão gerada: {sugestao}")

        except ValueError as e:
            logging.error(f"Erro de validação: {e}")
            error_message.value = f"Valor inválido: {e}"
        except Exception as e:
            logging.error(f"Erro ao gerar sugestão: {e}")
            error_message.value = "Erro ao processar. Verifique os logs."
        finally:
            progress_indicator.visible = False
            page.update()

    btn_gerar_sugestao = ft.ElevatedButton("Analisar Compra", on_click=gerar_sugestao)

    # Gráfico de Gastos por Categoria
    gastos_categoria = financial_analyzer.get_expenses_by_category()
    categorias = list(gastos_categoria.keys())
    valores = list(gastos_categoria.values())

    fig, ax = plt.subplots()
    ax.bar(categorias, valores)
    plt.xlabel("Categorias")
    plt.ylabel("Gastos (R$)")
    plt.title("Gastos por Categoria")
    plt.xticks(rotation=45, ha="right") # Rotação das labels do eixo X para melhor visualização
    plt.tight_layout() # Ajusta o layout para evitar sobreposição de elementos

    grafico_gastos = MatplotlibChart(fig, expand=True)

    # Layout da página
    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Bem-vindo ao OCB - Seu Analisador de Gastos!", size=20),
                        ft.Text("Insira os dados da compra:", size=16),
                        txt_valor,
                        txt_categoria,
                        btn_gerar_sugestao,
                        txt_sugestao,
                        progress_indicator,
                        error_message,
                    ],
                    width=400, #ajuste para o grafico
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.VerticalDivider(width=2, color="white"), #ajuste para o grafico
                grafico_gastos #ajuste para o grafico
            ],
            expand=True, #ajuste para o grafico
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

# Inicia o aplicativo Flet
ft.app(target=main)