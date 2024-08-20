# ocb/financial_analyzer.py
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class FinancialAnalyzer:
    """Analisa dados financeiros para fornecer insights."""

    def __init__(self, dados_resumo):
        """Inicializa com os dados da aba 'Resumo'."""
        self.dados_resumo = dados_resumo

    def get_current_balance(self):
        """Retorna o saldo restante."""
        try:
            saldo_restante = float(self.dados_resumo[1][5].replace(
                # Considerando o formato brasileiro
                '.', '').replace(',', '.'))
            return saldo_restante
        except (IndexError, ValueError):
            logging.error("Erro ao acessar 'Saldo_Restante' na planilha.")
            return 0.0

    def get_available_credit(self):
        """Retorna o limite de crédito disponível."""
        # Implemente a lógica para calcular o limite disponível
        # com base nos seus dados.
        # Por enquanto, retornaremos um valor fixo:
        limite_disponivel = 1500.00
        logging.info(f"Limite de crédito disponível: R$ {
                     limite_disponivel:.2f}")
        return limite_disponivel

    def calcular_limite_credito(self):
        """Calcula o limite de crédito estimado."""
        fator_limite = 3.0

        # Correção: Acessar 'Saldo_Restante' como lista
        try:
            saldo_restante = float(
                self.dados_resumo[1][5].replace('.', '').replace(',', '.'))
        except (IndexError, ValueError):
            logging.error("Erro ao acessar 'Saldo_Restante' na planilha.")
            saldo_restante = 0.0

        limite_estimado = saldo_restante * fator_limite
        logging.info(f"Limite de crédito estimado: R$ {limite_estimado:.2f}")
        return limite_estimado

    def simular_compra(self, valor_compra, parcelas):
        """Simula o impacto da compra no orçamento."""
        # ... (lógica de simulação) ...
        return impacto
