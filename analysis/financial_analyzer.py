"""Módulo responsável por analisar os dados financeiros e gerar sugestões."""

from typing import List, Dict

class FinancialAnalyzer:
    """Analisa os dados de gastos e gera sugestões de pagamento."""

    def __init__(self, expenses_data: List[Dict[str, str]]):
        """Inicializa o FinancialAnalyzer com os dados de despesas."""
        self.expenses_data = expenses_data
        self.category_limits = {  # Limites de gastos por categoria
            "Alimentação": 500,
            "Transporte": 300,
            "Lazer": 200,
            # Adicione outras categorias aqui
        }
        self.initial_balance = 2000  # Saldo inicial -  Vamos torná-lo dinâmico no futuro

    def calculate_current_balance(self) -> float:
        """Calcula o saldo atual."""
        total_expenses = sum(
            float(expense["Valor"]) for expense in self.expenses_data if expense["Tipo"] == "Despesa"
        )
        return self.initial_balance - total_expenses

    def get_category_expenses(self, category: str) -> float:
        """Retorna o total de gastos em uma categoria específica."""
        return sum(
            float(expense["Valor"])
            for expense in self.expenses_data
            if expense["Categoria"] == category
        )

    def suggest_payment_method(self, purchase_amount: float, category: str) -> str:
        """Sugere o método de pagamento com base no saldo, limite da categoria e valor da compra."""
        current_balance = self.calculate_current_balance()
        category_expenses = self.get_category_expenses(category)
        
        if (
            current_balance >= purchase_amount
            and category_expenses + purchase_amount <= self.category_limits.get(category, float("inf"))
        ):
            return "Compra aprovada no cartão! 😊"
        elif current_balance >= purchase_amount:
            return "Compra aprovada, mas considere usar dinheiro para esta categoria este mês. 🤔"
        else:
            return "Saldo insuficiente. Aguarde o próximo pagamento! 😔"

# Exemplo de uso no ocb/main.py
from ocb.data.data_loader import DataLoader
from ocb.analysis.financial_analyzer import FinancialAnalyzer

if __name__ == "__main__":
    # ... (código para carregar os dados da planilha)

    analyzer = FinancialAnalyzer(expenses_data)

    # Exemplo de uso da sugestão de pagamento
    purchase_amount = 100
    purchase_category = "Alimentação"
    suggestion = analyzer.suggest_payment_method(purchase_amount, purchase_category)
    print(f"Sugestão para compra de R${purchase_amount:.2f} na categoria '{purchase_category}': {suggestion}")