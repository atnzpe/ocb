"""Módulo responsável por analisar os dados financeiros e gerar sugestões."""

from typing import List, Dict
from .data_loader import DataLoader # Importe relativo

class FinancialAnalyzer:
    """Analisa os dados de gastos e gera informações financeiras."""

    def __init__(self, expenses_data: List[Dict[str, str]], initial_balance: float, credit_limit: float):
        """Inicializa o FinancialAnalyzer.

        Args:
            expenses_data (List[Dict[str, str]]): Dados de despesas da planilha.
            initial_balance (float): Saldo inicial.
            credit_limit (float): Limite do cartão de crédito.
        """
        self.expenses_data = expenses_data
        self.initial_balance = initial_balance
        self.credit_limit = credit_limit

    def get_current_balance(self) -> float:
        """Calcula o saldo atual."""
        total_expenses = sum(
            float(expense["Valor"])
            for expense in self.expenses_data
            if expense["Tipo"] == "Despesa"
        )
        total_income = sum(
            float(expense["Valor"])
            for expense in self.expenses_data
            if expense["Tipo"] == "Receita"
        )
        return self.initial_balance + total_income - total_expenses

    def get_available_credit(self) -> float:
        """Calcula o crédito disponível."""
        return self.credit_limit - self.get_total_expenses()

    def get_total_expenses(self) -> float:
        """Calcula o total de despesas."""
        return sum(
            float(expense["Valor"])
            for expense in self.expenses_data
            if expense["Tipo"] == "Despesa"
        )
    
    def get_total_income(self) -> float:
        """Calcula o total de receitas."""
        return sum(
            float(expense["Valor"])
            for expense in self.expenses_data
            if expense["Tipo"] == "Receita"
        )

    def get_expenses_by_category(self) -> Dict[str, float]:
        """Retorna um dicionário com o total de gastos por categoria."""
        expenses_by_category = {}
        for expense in self.expenses_data:
            if expense["Tipo"] == "Despesa":  # Considera apenas despesas
                category = expense["Categoria"]
                value = float(expense["Valor"])
                if category in expenses_by_category:
                    expenses_by_category[category] += value
                else:
                    expenses_by_category[category] = value
        return expenses_by_category