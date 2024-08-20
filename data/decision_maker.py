from .financial_analyzer import FinancialAnalyzer


class DecisionMaker:
    """Aplica as regras de decisão para sugestões de compra."""

    def __init__(
        self,
        financial_analyzer: FinancialAnalyzer,
        min_balance: float = 500.0,
        max_category_percentage: float = 0.3,
        installment_interest_rate: float = 0.02,
    ):  # Adicionado juros de parcelamento
        """Inicializa o DecisionMaker.

        Args:
            financial_analyzer (FinancialAnalyzer): Instância do FinancialAnalyzer.
            min_balance (float): Saldo mínimo necessário após a compra.
            max_category_percentage (float): Porcentagem máxima de gasto por categoria.
            installment_interest_rate (float): Taxa de juros mensal para parcelamento (padrão: 2%).
        """
        self.financial_analyzer = financial_analyzer
        self.min_balance = min_balance
        self.max_category_percentage = max_category_percentage
        self.installment_interest_rate = installment_interest_rate

    def get_purchase_suggestion(self, purchase_amount: float, category: str) -> str:
        """Gera sugestões de compra com base nas regras."""
        current_balance = self.financial_analyzer.get_current_balance()
        available_credit = self.financial_analyzer.get_available_credit()

        if current_balance - purchase_amount < self.min_balance:
            return "Compra negada: Saldo insuficiente."

        category_expenses = self.financial_analyzer.get_expenses_by_category().get(
            category, 0.0
        )
        if (
            category_expenses + purchase_amount
        ) / self.financial_analyzer.get_total_expenses() > self.max_category_percentage:
            return "Compra negada: Limite de categoria excedido."

        if purchase_amount > available_credit:
            return "Compra negada: Limite do cartão excedido."

        # Lógica de parcelamento (aprimorada com juros)
        if purchase_amount > available_credit / 3:
            installment_amount = self._calculate_installment(purchase_amount, 3)
            return f"Sugestão: Parcelar a compra em 3x de R${installment_amount:.2f} (com juros)."

        return "Compra aprovada no cartão!"

    def _calculate_installment(self, amount: float, installments: int) -> float:
        """Calcula o valor da parcela com juros compostos."""
        total_amount = amount * (1 + self.installment_interest_rate) ** installments
        return total_amount / installments
