# OCB - Organizador de Contas Brasileiro 🇧🇷

## Descrição

* Está cansado de planilhas confusas e falta de clareza nas suas finanças? O OCB (Organizador de Contas Brasileiro) é a solução que você precisava!

* Este projeto inovador utiliza o poder da Inteligência Artificial para te ajudar a tomar decisões financeiras mais inteligentes. O OCB analisa seus gastos e receitas diretamente da sua planilha Google Sheet, prevê seus limites de crédito e débito e te aconselha sobre a melhor forma de pagamento para novas compras.

* Imagine um assistente financeiro pessoal que te ajuda a:

* Visualizar suas finanças: Importe facilmente seus dados de uma planilha Google Sheets organizada em abas "Resumo", "Receita" e "Despesa".

* Prever seus limites: Um modelo de Machine Learning inteligente analisa seu histórico para prever seus limites de crédito e débito com precisão.

* Tomar decisões de compra inteligentes: Forneça detalhes sobre uma compra e o OCB, usando o poder do GPT-2, recomenda a melhor forma de pagamento (à vista, parcelado, cartão ou dinheiro) considerando seus limites e histórico.

* Saber quando você pode comprar: Se você não puder fazer uma compra agora, o OCB te dirá quando você poderá, baseado na análise da sua planilha.

## Demonstração

Visualize o OCB em ação! ![GIF da interface do aplicativo em funcionamento](./assets/ocb_demo.gif)  

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

1. Organização da Planilha: Certifique-se de que sua planilha Google Sheets esteja estruturada com as abas "Resumo", "Receita" e "Despesa", contendo colunas para data, descrição, valor e categoria.

2. Conecte e Explore: Execute o aplicativo e conecte-se à sua conta Google para carregar sua planilha.

3. Simule Compras: Insira os detalhes da compra que você deseja fazer e receba a recomendação do OCB sobre a melhor forma de pagamento!



## Tecnologias utilizadas 💻

* **Python:** Linguagem de programação principal.
* **Flet:** Framework para criação da interface web.
* **Google Sheets API:** Acesso aos dados da planilha.
* **GPT-2:** Modelo de linguagem para sugestões personalizadas.
* **Scikit-learn:** Biblioteca de Machine Learning para previsão de limites.

## Próximos passos 🚧

- [ ] Interface ainda mais rica: Gráficos interativos e visualizações para melhor acompanhamento das suas finanças.
- [ ] Testes unitários abrangentes: Garantia da qualidade e confiabilidade do código.
- [ ] Modelos de IA ainda mais inteligentes: Explorar modelos mais avançados para sugestões ainda mais precisas e personalizadas.
- [ ] Personalização completa: Permitir que o usuário ajuste as regras de decisão e os parâmetros do modelo de acordo com suas preferências.

## Contribuindo 💪

Sinta-se à vontade para contribuir com o projeto! 

1. Faça um fork do repositório.
2. Crie uma branch para sua feature: `git checkout -b minha-feature`
3. Faça o commit das suas alterações: `git commit -am 'Adiciona nova funcionalidade'`
4. Faça o push para sua branch: `git push origin minha-feature`
5. Abra um Pull Request.

## Licença 📄

Apache License 2.0