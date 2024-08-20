from typing import List, Dict
from .financial_analyzer import FinancialAnalyzer
from transformers import pipeline


class DecisionMaker:
    """Aplica as regras de decisão para sugestões de compra."""

    def __init__(
        self,
        financial_analyzer: FinancialAnalyzer,
        min_balance: float = 500.0,
        max_category_percentage: float = 0.3,
    ):
        """Inicializa o DecisionMaker.

        Args:
            financial_analyzer (FinancialAnalyzer): Instância do FinancialAnalyzer.
            min_balance (float): Saldo mínimo necessário após a compra.
            max_category_percentage (float): Porcentagem máxima de gasto por categoria.
        """
        self.financial_analyzer = financial_analyzer
        self.min_balance = min_balance
        self.max_category_percentage = max_category_percentage

    def get_purchase_suggestion(self, purchase_amount: float, category: str) -> str:
        """Gera sugestões de compra personalizadas usando GPT-2."""
        current_balance = self.financial_analyzer.get_current_balance()
        available_credit = self.financial_analyzer.get_available_credit()
        total_income = self.financial_analyzer.get_total_income()

        if current_balance - purchase_amount < self.min_balance:
            return "Compra negada: Saldo insuficiente."

        category_limit = total_income * self.max_category_percentage
        category_expenses = self.financial_analyzer.get_expenses_by_category().get(
            category, 0.0
        )
        if (category_expenses + purchase_amount) > category_limit:
            return (
                f"Compra negada: Limite da categoria ({category_limit:.2f}) excedido."
            )

        if purchase_amount > available_credit:
            return "Compra negada: Limite do cartão excedido."

        # Gerar sugestão com GPT-2
        generator = pipeline("text-generation", model="gpt2")
        prompt = (
            f"Desejo comprar um item de R${purchase_amount:.2f} na categoria '{category}'. "
            f"Meu saldo atual é R${self.financial_analyzer.get_current_balance():.2f} e "
            f"meu limite disponível no cartão é R${self.financial_analyzer.get_available_credit():.2f}. "
            f"O que você sugere?"
        )

        suggestion = generator(prompt, max_length=100, num_return_sequences=1)[0][
            "generated_text"
        ]

        return suggestion.strip()
