from typing import List, Dict
from .financial_analyzer import FinancialAnalyzer
from transformers import pipeline

class DecisionMaker:
    """Aplica as regras de decisão para sugestões de compra."""

    def __init__(self, financial_analyzer: FinancialAnalyzer, 
                 min_balance: float = 500.0, max_category_percentage: float = 0.3):
        """Inicializa o DecisionMaker.

        Args:
            financial_analyzer (FinancialAnalyzer): Instância do FinancialAnalyzer.
            min_balance (float): Saldo mínimo necessário após a compra.
            max_category_percentage (float): Porcentagem máxima de gasto por categoria.
        """
        self.financial_analyzer = financial_analyzer
        self.min_balance = min_balance
        self.max_category_percentage = max_category_percentage
    
    def get_purchase_suggestion(self, purchase_amount: float, category: str) -> dict:
        """Gera sugestões de compra personalizadas e extrai informações relevantes."""

        # Gerar sugestão com GPT-2
        generator = pipeline('text-generation', model='gpt2')

        prompt = f"""
        Saldo atual: R$ {self.financial_analyzer.get_current_balance():.2f}
        Limite do cartão: R$ {self.financial_analyzer.get_available_credit():.2f}
        Compra: R$ {purchase_amount:.2f} em {category}

        Posso realizar essa compra? Em caso positivo, qual a melhor forma de pagamento?
        """

        suggestion = generator(prompt, max_length=100, num_return_sequences=1)[0]['generated_text']

        # Processar a resposta do GPT-2
        suggestion = self._extract_suggestion(suggestion)
        justification = self._extract_justification(suggestion)

        return {"suggestion": suggestion, "justification": justification}

    def _extract_suggestion(self, text: str) -> str:
        """Extrai a sugestão de compra (aprovada/negada, parcelamento)."""
        # Lógica simples para encontrar palavras-chave
        if "sim" in text.lower() or "aprovada" in text.lower():
            if "parcelar" in text.lower():
                return "Compra aprovada! Sugestão: parcelar a compra."
            else:
                return "Compra aprovada!"
        else:
            return "Compra negada!"  

    def _extract_justification(self, text: str) -> str:
        """Extrai a justificativa da sugestão."""
        # Lógica simples para extrair a parte após "pois" ou "porque"
        for keyword in ["pois", "porque"]:
            if keyword in text.lower():
                return text.split(keyword, 1)[1].strip()
        return "Sem justificativa."