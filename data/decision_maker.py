from .financial_analyzer import FinancialAnalyzer  # Importe a classe correta


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
        """Gera sugestões de compra com base nas regras.

        Args:
            purchase_amount (float): Valor da compra.
            category (str): Categoria da compra.

        Returns:
            str: Sugestão de compra (ex: "Compra aprovada!", "Parcelar em 3x", etc.).
        """

        current_balance = self.financial_analyzer.get_current_balance()
        available_credit = self.financial_analyzer.get_available_credit()
        total_income = (
            self.financial_analyzer.get_total_income()
        )  # Usaremos a renda total para calcular o limite da categoria

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

        # Lógica de parcelamento (aprimorada)
        max_installments = 12  # Número máximo de parcelas
        min_installment_value = 50.0  # Valor mínimo por parcela

        if (
            purchase_amount > available_credit / 3
        ):  # Simplificando a regra de parcelamento
            for installments in range(2, max_installments + 1):
                installment_value = purchase_amount / installments
                if (
                    installment_value <= available_credit / installments
                    and installment_value >= min_installment_value
                ):
                    return f"Sugestão: Parcelar a compra em {installments}x de R${installment_value:.2f}"

        return "Compra aprovada no cartão!"
