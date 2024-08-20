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
        """Gera sugestões de compra personalizadas usando o GPT-2."""

        # Gerar sugestão com GPT-2
        generator = pipeline("text-generation", model="gpt2")

        prompt = f"""
        Saldo atual: R$ {self.financial_analyzer.get_current_balance():.2f}
        Limite do cartão: R$ {self.financial_analyzer.get_available_credit():.2f}
        Compra: R$ {purchase_amount:.2f} em {category}

        Posso realizar essa compra? Em caso positivo, qual a melhor forma de pagamento?
        """

        suggestion = generator(prompt, max_length=100, num_return_sequences=1)[0][
            "generated_text"
        ]
        return suggestion.strip()
