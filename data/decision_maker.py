from typing import Dict
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import logging


class DecisionMaker:
    """
    Classe para gerar sugestões de compra personalizadas com base 
    em regras financeiras. 
    """

    def __init__(self):
        """Inicializa o DecisionMaker e carrega os modelos de IA."""
        logging.info("Inicializando DecisionMaker...")
        try:
            logging.info("Carregando modelo de sentimento...")
            self.sentiment_model = AutoModelForSequenceClassification.from_pretrained(
                "nlptown/bert-base-multilingual-uncased-sentiment")
            self.tokenizer = AutoTokenizer.from_pretrained(
                "nlptown/bert-base-multilingual-uncased-sentiment")
            logging.info("Modelo de sentimento carregado com sucesso!")
        except Exception as e:
            logging.error(f"Erro ao carregar o modelo de sentimento: {e}")
            self.sentiment_model = None
            self.tokenizer = None

    def get_purchase_suggestion(self, saldo_atual: float, limite_credito: float,
                                impacto_compra: str, valor_compra: float,
                                parcelas: int, forma_pagamento: str) -> Dict[str, str]:
        
        '''
        
            Gera sugestões de compra com base em regras financeiras.

            Args:
                saldo_atual (float): Saldo restante da conta.
                limite_credito (float): Limite de crédito disponível.
                impacto_compra (str): Descrição do impacto da compra no orçamento.
                valor_compra (float): Valor total da compra.
                parcelas (int): Número de parcelas.
                forma_pagamento (str): Forma de pagamento selecionada.

            Returns:
                Dict[str, str]: Um dicionário contendo a sugestão e a justificativa.
                
        '''
            
        try:
            # Formata o prompt para o GPT-2
            prompt = f""" 
                Compra de R$ {valor_compra: .2f} em {parcelas}x no {forma_pagamento}.
                Saldo atual: R$ {saldo_atual: .2f}
                Limite de crédito: R$ {limite_credito: .2f}
                Impacto da compra no orçamento: {impacto_compra}
                

                
                """
            
            # Regra: Compra aprovada se o valor for menor ou igual a 30% do saldo atual
            if valor_compra <= 0.30 * saldo_atual:
                quest = prompt
                suggestion = "Compra aprovada!"
                justification = "O valor da compra está dentro do limite de 30% do seu saldo atual."
            else:
                quest = prompt
                suggestion = "Compra negada!"
                justification = "O valor da compra ultrapassa o limite de 30% do seu saldo atual."
            
            '''
            > Se usar Chat GPT use este trecho para enviar
            logging.info(f"Prompt enviado ao GPT-2: {prompt}")

            # Gera texto com o GPT-2
            generator = pipeline("text-generation", model="gpt2")
            response = generator(prompt, max_new_tokens=50, num_return_sequences=1)[0]["generated_text"]
            logging.info(f"Resposta do GPT-2: {response}")
            '''

            return {
                "resume":prompt,
                "suggestion": suggestion, #Para analise de sentimento com ML use self._extract_suggestion(response),
                "justification": justification #Para analise de sentimento com ML useself._extract_justification(response)
            }

        except Exception as e:
            logging.error(f"Erro ao gerar sugestão: {e}")
            return {"suggestion": "Erro ao processar.", "justification": "Verifique os logs."}

'''
#No futuro a analise de sentimento sera feita atraves do nosso Modelo de ML usado no arquivo prediction_model

    def _extract_suggestion(self, text: str) -> str:
        """
        Extrai a sugestão da resposta do GPT-2 usando análise de sentimentos.

        Args:
            text (str): Resposta do GPT-2.

        Returns:
            str: Sugestão extraída (Aprovada, Negada, etc.).
        """

        if self.sentiment_model is None or self.tokenizer is None:
            logging.error("Modelo de sentimento não carregado.")
            return "Erro ao processar."

        try:
            # Análise de Sentimentos com modelo pré-treinado
            inputs = self.tokenizer(text, return_tensors='pt')
            with torch.no_grad():
                outputs = self.sentiment_model(**inputs)
            
            sentiment = int(torch.argmax(outputs.logits)) + 1

            # Define a sugestão com base no sentimento
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
            text (str): Resposta do GPT-2.

        Returns:
            str: Justificativa extraída da resposta.
        """
        for keyword in ["pois", "porque"]:
            if keyword in text.lower():
                return text.split(keyword, 1)[1].strip()
        return "Sem justificativa explícita."

'''