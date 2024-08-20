# ocb/decision_maker.py
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import torch
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DecisionMaker:
    def __init__(self):
        """Inicializa o DecisionMaker e carrega o modelo de sentimento."""
        logging.info("Inicializando DecisionMaker.")
        try:
            self.sentiment_model = AutoModelForSequenceClassification.from_pretrained(
                'nlptown/bert-base-multilingual-uncased-sentiment')
            self.tokenizer = AutoTokenizer.from_pretrained(
                'nlptown/bert-base-multilingual-uncased-sentiment')
            logging.info("Modelo de sentimento carregado com sucesso!")
        except Exception as e:
            logging.error(f"Erro ao carregar modelo de sentimento: {e}")
            self.sentiment_model = None
            self.tokenizer = None

    def get_purchase_suggestion(self, saldo_atual: float, limite_credito: float, impacto_compra,
                                 valor_compra: float, parcelas: int, forma_pagamento: str):
        """Gera sugestões de compra usando o LLM (GPT-2)."""
        try:
            prompt = f"""
            Saldo atual: R$ {saldo_atual:.2f}
            Limite de crédito: R$ {limite_credito:.2f}
            Impacto da compra no orçamento: {impacto_compra}
            Compra de R$ {valor_compra:.2f} em {parcelas}x no {forma_pagamento}.

            Posso realizar essa compra? Sugira a melhor forma de pagamento e quando 
            devo comprar se não for possível agora. 
            """
            logging.info(f"Prompt enviado ao GPT-2: {prompt}")
            generator = pipeline("text-generation", model="gpt2")
            response = generator(prompt, max_new_tokens=50, num_return_sequences=1)[0]["generated_text"]
            logging.info(f"Resposta do GPT-2: {response}")

            return {
                "suggestion": self._extract_suggestion(response),
                "justification": self._extract_justification(response)
            }
        except Exception as e:
            logging.error(f"Erro ao gerar sugestão: {e}")
            return {"suggestion": "Erro ao processar.", "justification": "Verifique os logs."}

    def _extract_suggestion(self, text: str) -> str:
        """Extrai a sugestão da resposta do GPT-2."""
        if self.sentiment_model is None or self.tokenizer is None:
            logging.error("Modelo de sentimento não carregado.")
            return "Erro ao processar."
        try:
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
        """Extrai a justificativa da resposta do GPT-2."""
        for keyword in ["pois", "porque"]:
            if keyword in text.lower():
                return text.split(keyword, 1)[1].strip()
        return "Sem justificativa explícita."