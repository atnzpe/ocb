"""Módulo responsável por analisar os dados financeiros e gerar sugestões."""

from typing import List, Dict
from .data_loader import DataLoader
from datetime import datetime, timedelta


class FinancialAnalyzer:
    """Analisa os dados de gastos e fornece informações financeiras."""

    def __init__(
        self, data_loader: DataLoader, initial_balance: float, credit_limit: float
    ):
        """Inicializa o FinancialAnalyzer.

        Args:
            data_loader (DataLoader): Instância do DataLoader.
            initial_balance (float): Saldo inicial da conta.
            credit_limit (float): Limite total do cartão de crédito.
        """
        self.data_loader = data_loader
        self.expenses_data = self.data_loader.load_data()
        self.initial_balance = initial_balance
        self.credit_limit = credit_limit

    def get_expenses_by_category(self) -> Dict[str, float]:
        """Calcula o total de gastos por categoria."""
        expenses_by_category = {}
        for expense in self.expenses_data:
            category = expense.get("Categoria")
            amount = float(expense.get("Valor", 0.0))  # Trata valores inválidos
            if category:
                expenses_by_category[category] = (
                    expenses_by_category.get(category, 0.0) + amount
                )
        return expenses_by_category

    def get_total_expenses(self) -> float:
        """Calcula o total de gastos."""
        return sum([float(expense.get("Valor", 0.0)) for expense in self.expenses_data])

    def get_current_balance(self) -> float:
        """Calcula o saldo atual."""
        return self.initial_balance - self.get_total_expenses()

    def get_available_credit(self) -> float:
        """Calcula o limite disponível no cartão."""
        return self.credit_limit - self.get_total_expenses_credit_card()

    def get_average_expenses_per_period(self, period: str = "month") -> float:
        """Calcula a média de gastos por semana ou mês."""
        total_expenses = self.get_total_expenses()
        if period == "week":
            num_weeks = (datetime.now() - self._get_first_expense_date()).days // 7
            return (
                total_expenses / num_weeks if num_weeks else 0
            )  # Evita divisão por zero
        elif period == "month":
            num_months = (
                datetime.now().year - self._get_first_expense_date().year
            ) * 12 + (datetime.now().month - self._get_first_expense_date().month)
            return (
                total_expenses / num_months if num_months else 0
            )  # Evita divisão por zero
        else:
            raise ValueError("Período inválido. Use 'week' ou 'month'.")

    # Funções auxiliares
    def get_total_expenses_credit_card(self) -> float:
        """Calcula o total de gastos no cartão de crédito."""
        return sum(
            [
                float(expense.get("Valor", 0.0))
                for expense in self.expenses_data
                if expense.get("Forma de Pagamento") == "Cartão"
            ]
        )

    def _get_first_expense_date(self) -> datetime:
        """Retorna a data do primeiro gasto da lista."""
        try:
            dates = [
                datetime.strptime(expense["Data"], "%d/%m/%Y")
                for expense in self.expenses_data
                if expense.get("Data")
            ]
            return min(dates) if dates else datetime.now()
        except ValueError:
            return datetime.now()
