# OCB - Organizador de Contas Brasileiro 🇧🇷

## Descrição

Este projeto te auxiliará na tomada de decisões financeiras inteligentes! O OCB analisa seus gastos e receitas em uma planilha Google Sheet, prevê seus limites de crédito e débito usando Machine Learning e sugere a melhor forma de pagamento para suas compras com um modelo de linguagem de última geração (GPT-2).

**Funcionalidades:**

* Importa dados de receitas e despesas de uma planilha Google Sheets.
* **Prevê limites de crédito e débito usando um modelo de Machine Learning treinado com seus dados.**
* **Gera sugestões personalizadas de pagamento (cartão, dinheiro, parcelamento) com base no GPT-2, considerando seu histórico financeiro.**
* Interface web intuitiva e fácil de usar, criada com Python e Flet.

## Demonstração

![GIF da interface do aplicativo em funcionamento](./assets/ocb_demo.gif)  

## Como começar 🚀

1. **Clone o repositório:**

git clone https://github.com/atnzpe/ocb


2. **Crie e ative um ambiente virtual:**

python -m venv .venv source .venv/bin/activate

3. **Instale as dependências:**

pip install -r requirements.txt

4. **Configure suas credenciais do Google Sheets:**
   - Crie um projeto na Google Cloud Platform e ative a API do Google Sheets.
   - Gere um arquivo de credenciais JSON (instruções [aqui](https://developers.google.com/sheets/api/quickstart/python)) e coloque-o na pasta `ocb/` (**NÃO** adicione este arquivo ao Git!).
5. **Execute o aplicativo:**

 python ocb/main.py

## Uso

1. Certifique-se de que sua planilha Google Sheets esteja organizada com abas separadas para "Receitas" e "Despesas", contendo colunas para data, descrição, valor e categoria.
2. Execute o aplicativo. O OCB irá:
   - Carregar seus dados de receitas e despesas da planilha.
   - Treinar um modelo de Machine Learning para prever seus limites de crédito e débito.
   - Exibir os limites previstos na interface do usuário.
   - Permitir que você insira o valor e a categoria de uma nova compra.
   - Gerar uma sugestão de pagamento personalizada, considerando seus limites e histórico financeiro.

## Exemplos

**Previsão de Limites:**

- Limite de Crédito Previsto: R$ 5.000,00
- Limite de Débito Previsto: R$ 1.500,00

**Sugestão de Pagamento:**

- Valor da compra: R$ 200,00
- Categoria: Restaurante

> Sugestão: Pagar com cartão de débito.

## Tecnologias utilizadas 💻

* **Python:** Linguagem de programação principal.
* **Flet:** Framework para criação da interface web.
* **Google Sheets API:** Acesso aos dados da planilha.
* **GPT-2:** Modelo de linguagem para sugestões personalizadas.
* **Scikit-learn:** Biblioteca de Machine Learning para previsão de limites.

## Próximos passos 🚧

- Aprimorar a interface do usuário com gráficos e visualizações interativas.
- Implementar testes unitários para garantir a qualidade do código.
- Explorar modelos de IA mais avançados para gerar sugestões ainda mais precisas.
- Permitir que o usuário personalize as regras de decisão e os parâmetros do modelo.

## Contribuindo 💪

Sinta-se à vontade para contribuir com o projeto! 

1. Faça um fork do repositório.
2. Crie uma branch para sua feature: `git checkout -b minha-feature`
3. Faça o commit das suas alterações: `git commit -am 'Adiciona nova funcionalidade'`
4. Faça o push para sua branch: `git push origin minha-feature`
5. Abra um Pull Request.

## Licença 📄

Apache License 2.0