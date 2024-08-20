from typing import List, Dict
from .financial_analyzer import FinancialAnalyzer
from transformers import pipeline
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DecisionMaker:
    """
    Analisa dados financeiros e gera sugestões de compra inteligentes usando IA.
    """

    def __init__(
        self,
        financial_analyzer: FinancialAnalyzer,
        min_balance: float = 500.0,
        max_category_percentage: float = 0.3,
    ):
        """
        Inicializa o DecisionMaker.

        Args:
            financial_analyzer: Instância do FinancialAnalyzer para acesso aos dados financeiros.
            min_balance: Saldo mínimo desejável após a compra.
            max_category_percentage: Porcentagem máxima do limite disponível permitida para gastos em uma categoria.
        """
        logging.info("Inicializando DecisionMaker.")
        self.financial_analyzer = financial_analyzer
        self.min_balance = min_balance
        self.max_category_percentage = max_category_percentage

        # Carrega o modelo de análise de sentimentos
        self.sentiment_model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
        self.tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

    def get_purchase_suggestion(self, purchase_amount: float, category: str) -> dict:
        """
        Gera sugestões personalizadas, analisando o contexto financeiro e o sentimento.

        Args:
            purchase_amount: Valor da compra.
            category: Categoria da compra.

        Returns:
            Um dicionário contendo a sugestão de compra e a justificativa.
        """
        try:
            # Gera sugestão textual usando GPT-2
            generator = pipeline("text-generation", model="gpt2")
            prompt = f"""
            Saldo atual: R$ {self.financial_analyzer.get_current_balance():.2f}
            Limite do cartão: R$ {self.financial_analyzer.get_available_credit():.2f}
            Compra: R$ {purchase_amount:.2f} em {category}

            Posso realizar essa compra? Em caso positivo, qual a melhor forma de pagamento?
            """
            logging.info(f"Prompt enviado ao GPT-2: {prompt}")
            response = generator(prompt, max_new_tokens=50, num_return_sequences=1)[0]["generated_text"]
            logging.info(f"Resposta do GPT-2: {response}")

            # Extrai a sugestão e justificativa da resposta
            suggestion = self._extract_suggestion(response)
            justification = self._extract_justification(response)

            return {"suggestion": suggestion, "justification": justification}
        except Exception as e:
            logging.error(f"Erro ao gerar sugestão: {e}")
            return {"suggestion": "Erro ao processar.", "justification": "Verifique os logs."}

    def _extract_suggestion(self, text: str) -> str:
        """
        Extrai a sugestão da resposta do GPT-2 usando análise de sentimento.

        Args:
            text: Resposta textual do GPT-2.

        Returns:
            Uma string contendo a sugestão extraída.
        """
        try:
            # Analisa o sentimento da resposta
            inputs = self.tokenizer(text, return_tensors='pt')
            with torch.no_grad():
                outputs = self.sentiment_model(**inputs)
            sentiment = int(torch.argmax(outputs.logits)) + 1 

            if sentiment >= 4:
                if "parcelar" in text.lower() and "não" not in text.lower():
                    return "Compra aprovada! Sugestão: parcelar."
                else:
                    return "Compra aprovada!"
            elif sentiment == 3:
                return "Compra aprovada! Mas analise bem a compra."
            else:
                return "Compra negada!"

        except Exception as e:
            logging.error(f"Erro ao extrair sugestão: {e}")
            return "Erro ao processar."

    def _extract_justification(self, text: str) -> str:
        """
        Extrai a justificativa da resposta do GPT-2.

        Args:
            text: Resposta textual do GPT-2.

        Returns:
            Uma string contendo a justificativa extraída.
        """
        for keyword in ["pois", "porque"]:
            if keyword in text.lower():
                return text.split(keyword, 1)[1].strip()
        return "Sem justificativa explícita."