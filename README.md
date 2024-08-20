# OCB - Organizador de Contas Brasileiro 🇧🇷

## Descrição

Este projeto te auxiliará na tomada de decisões financeiras inteligentes! O OCB analisa seus gastos em uma planilha Google Sheet e sugere a melhor forma de pagamento para suas compras. 

**Funcionalidades:**

* Importe seus dados de gastos de uma planilha Google Sheets.
* Defina suas próprias regras de decisão para compras (ex: limite de gastos por categoria).
* Receba sugestões personalizadas de pagamento (cartão, dinheiro, parcelamento) com base em um modelo de IA.
* Interface web intuitiva e fácil de usar, criada com Python e Flet.

## Como começar 🚀

1. **Clone o repositório:**

git clone https://github.com/atnzpe/ocb


2. **Crie e ative um ambiente virtual:**

python3 -m venv .venv source .venv/bin/activate

3. **Instale as dependências:**

pip install -r requirements.txt

4. **Configure suas credenciais do Google Sheets:**
   * Crie um projeto na Google Cloud Platform e ative a API do Google Sheets.
   * Gere um arquivo de credenciais JSON (instruções acima) e coloque-o na pasta `ocb/` (NÃO adicione este arquivo ao Git!).
5. **Execute o aplicativo:**

 python ocb/main.py



 ## Tecnologias utilizadas 💻

* **Python:** Linguagem de programação principal.
* **Flet:** Framework para criação da interface web.
* **Google Sheets API:** Acesso aos dados da planilha.
* **GPT-2:** Modelo de linguagem para sugestões personalizadas.

## Próximos passos 🚧

* [x] Implementar a leitura de dados da planilha Google Sheets.
* [x] Desenvolver a lógica de análise de gastos e regras de decisão.
* Integrar o modelo de linguagem (LLM) para gerar sugestões de pagamento.
* Criar a interface web com Flet.

## Contribuindo 💪

Sinta-se à vontade para contribuir com o projeto! 

1. Faça um fork do repositório.
2. Crie uma branch para sua feature: `git checkout -b minha-feature`
3. Faça o commit das suas alterações: `git commit -am 'Adiciona nova funcionalidade'`
4. Faça o push para sua branch: `git push origin minha-feature`
5. Abra um Pull Request.

## Licença 📄

Apache License  2.0