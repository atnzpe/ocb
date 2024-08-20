"""Módulo responsável por analisar os dados financeiros e gerar sugestões."""

from typing import List, Dict
from datetime import datetime
import pandas as pd


class FinancialAnalyzer:
    """Analisa os dados de gastos e fornece informações financeiras."""

    def __init__(
        self,
        expenses_data: List[Dict[str, str]],
        initial_balance: float,
        credit_limit: float,
    ):
        """Inicializa o FinancialAnalyzer.

        Args:
            expenses_data (List[Dict[str, str]]): Dados de despesas da planilha.
            initial_balance (float): Saldo inicial da conta.
            credit_limit (float): Limite total do cartão de crédito.
        """
        self.expenses_data = expenses_data
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
        total_expenses = sum(
            float(expense.get("Valor", 0.0))
            for expense in self.expenses_data
            if expense.get("Tipo") == "Despesa"
        )
        total_income = sum(
            float(expense.get("Valor", 0.0))
            for expense in self.expenses_data
            if expense.get("Tipo") == "Receita"
        )
        return self.initial_balance + total_income - total_expenses

    def get_available_credit(self) -> float:
        """Calcula o limite disponível no cartão."""
        return self.credit_limit - self.get_total_expenses()

    def get_average_expenses_per_period(self, period: str = "month") -> float:
        """Calcula a média de gastos por semana ou mês usando pandas."""
        df = pd.DataFrame(self.expenses_data)
        df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")
        df["Valor"] = df["Valor"].str.replace(",", ".").astype(float)

        if period == "week":
            return (
                df[df["Tipo"] == "Despesa"]
                .resample("W", on="Data")["Valor"]
                .mean()
                .iloc[-1]
            )
        elif period == "month":
            return (
                df[df["Tipo"] == "Despesa"]
                .resample("M", on="Data")["Valor"]
                .mean()
                .iloc[-1]
            )
        else:
            raise ValueError("Período inválido. Use 'week' ou 'month'.")

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
