from data.data_loader import DataLoader
import logging

class FinancialAnalyzer:
    """
    Analisa dados financeiros para fornecer informações sobre o orçamento,
    limite de crédito e simulação de compras.
    """

    def __init__(self, data_loader: DataLoader):
        """
        Inicializa o FinancialAnalyzer com os dados carregados.

        Args:
            data_loader: Instância de DataLoader com os dados da planilha.
        """
        self.data_loader = data_loader
        self.dados_resumo = self.data_loader.load_data("resumo") # Assume que 'resumo' é o nome da aba

    def get_current_balance(self):
        """
        Retorna o saldo restante da conta.

        Returns:
            float: Saldo restante da conta, ou 0.0 em caso de erro.
        """
        try:
            saldo_restante = float(self.dados_resumo[1][4].replace('.', '').replace(',', '.'))
            return saldo_restante
        except (IndexError, ValueError) as e:
            logging.error(f"Erro ao acessar 'Saldo_Restante' na planilha: {e}")
            return 0.0

    def get_available_credit(self):
        """
        Retorna o limite de crédito disponível.

        Returns:
            float: Limite de crédito disponível, ou 0.0 em caso de erro.
        """
        try:
            limite_total = float(self.dados_resumo[0][1].replace('.', '').replace(',', '.'))
            total_a_pagar = float(self.dados_resumo[0][6].replace('.', '').replace(',', '.'))
            limite_disponivel = limite_total - total_a_pagar
            logging.info(f"Limite de crédito disponível: R$ {limite_disponivel:.2f}")
            return limite_disponivel
        except (IndexError, ValueError) as e:
            logging.error(f"Erro ao acessar dados de crédito na planilha: {e}")
            return 0.0

    def simular_compra(self, valor_compra, parcelas):
        """
        Simula o impacto de uma compra no orçamento.

        Args:
            valor_compra (float): Valor total da compra.
            parcelas (int): Número de parcelas.

        Returns:
            str: Descrição do impacto da compra no orçamento.
        """
        saldo_atual = self.get_current_balance()
        valor_parcela = valor_compra / parcelas

        impacto = "Compra à vista "
        if saldo_atual >= valor_compra:
            impacto += "possível!" 
        else:
            impacto += "indisponível. "

        impacto += f"Parcelas de R$ {valor_parcela:.2f} por {parcelas} meses. "

        novo_saldo = saldo_atual - valor_compra
        impacto += f"Seu saldo após a compra seria de R$ {novo_saldo:.2f}."

        return impacto