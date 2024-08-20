import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from typing import List, Dict
import logging

# Configurar o logger para exibir mensagens informativas
logging.basicConfig(level=logging.INFO)


class PredictionModel:
    """
    Treina e utiliza um modelo de Machine Learning para prever limites de crédito e débito.
    """

    def __init__(self, receitas: List[Dict], despesas: List[Dict], resumo: List[Dict]):
        """
        Inicializa o PredictionModel.

        Args:
            receitas: Lista de dicionários contendo dados de receitas.
            despesas: Lista de dicionários contendo dados de despesas.
            resumo: Lista de dicionários contendo dados do resumo.
        """
        logging.info("Inicializando modelo de previsão.")
        self.receitas = pd.DataFrame(receitas)
        self.despesas = pd.DataFrame(despesas)
        self.resumo = pd.DataFrame(resumo)
        # Treinar os modelos durante a inicialização
        self.model_credito = self._train_model("credit_limit")
        self.model_debito = self._train_model("debit_limit")

    def _prepare_data(self) -> pd.DataFrame:
        """
        Prepara os dados para o treinamento do modelo.

        Returns:
            pd.DataFrame: DataFrame com as features de entrada para o modelo.
        """

        # Converter as colunas 'Valor' para numérico, tratando erros
        self.receitas['Valor'] = pd.to_numeric(
            self.receitas['Valor'], errors='coerce')
        self.despesas['Valor'] = pd.to_numeric(
            self.despesas['Valor'], errors='coerce')

        # Calcula o total de receitas e despesas
        total_receitas = self.receitas['Valor'].sum()
        total_despesas = self.despesas['Valor'].sum()

        # Crie um DataFrame com as features
        data = pd.DataFrame({
            'total_receitas': [total_receitas],
            'total_despesas': [total_despesas],
            # Adicione outras features relevantes aqui, como médias, proporções, etc.
        })

        # Extraia os valores das colunas e converta para float
        data['credit_limit'] = float(self.resumo['credit_limit'].iloc[0].replace(
            ',', '.')) if 'credit_limit' in self.resumo else None
        data['debit_limit'] = float(self.resumo['debit_limit'].iloc[0].replace(
            ',', '.')) if 'debit_limit' in self.resumo else None

        return data

    def _train_model(self, target_column: str) -> LinearRegression:
        """
        Treina um modelo de regressão linear para prever o limite de crédito ou débito.

        Args:
            target_column: Nome da coluna alvo no DataFrame de dados ('credit_limit' ou 'debit_limit').

        Returns:
            LinearRegression: Modelo treinado.
        """
        data = self._prepare_data()

        # Verificar se a coluna alvo existe
        if target_column not in data.columns:
            raise ValueError(
                f"Coluna alvo '{target_column}' não encontrada nos dados.")

        # Adaptar as features conforme necessário
        features = ["total_receitas", "total_despesas"]
        X = data[features]

        # Defina a coluna alvo (limite de crédito ou débito)
        y = data[target_column]

        # Divisão treino/teste
        X_train, _, y_train, _ = train_test_split(
            X, y, test_size=0.2, random_state=42)

        # Criação e treinamento do modelo
        model = LinearRegression()
        model.fit(X_train, y_train)

        return model

    def predict_limits(self) -> (float, float):
        """
        Prevê os limites de crédito e débito.

        Returns:
            Tuple[float, float]: Limite de crédito previsto, Limite de débito previsto.
        """

        # Utiliza os modelos já treinados na inicialização
        data = self._prepare_data()
        limite_credito = self.model_credito.predict(
            data[["total_receitas", "total_despesas"]])[0]
        limite_debito = self.model_debito.predict(
            data[["total_receitas", "total_despesas"]])[0]

        return limite_credito, limite_debito