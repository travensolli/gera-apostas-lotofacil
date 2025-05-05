# Projeto Lotofácil

Este projeto foi desenvolvido para realizar análises estatísticas e gerar combinações de apostas para a Lotofácil, utilizando dados históricos e integração com a API da OpenAI.

## Estrutura do Projeto Atualizada

```
gera-apostas-lotofacil/
├── lotofacil_data.json
├── README.md
├── requirements.txt
├── backend/
│   ├── api/
│   │   ├── fetch_lotofacil_data.py
│   │   ├── main.py
│   ├── database/
│   │   ├── lotofacil.db
│   │   ├── setup_database.py
│   ├── scripts/
│   │   ├── analyze_and_generate_combinations.py
│   │   ├── generate_accuracy_report.py
├── frontend/
│   ├── lotofacil-frontend/
│   │   ├── package.json
│   │   ├── README.md
│   │   ├── public/
│   │   │   ├── favicon.ico
│   │   │   ├── index.html
│   │   │   ├── logo192.png
│   │   │   ├── logo512.png
│   │   │   ├── manifest.json
│   │   │   ├── robots.txt
│   │   ├── src/
│   │   │   ├── App.css
│   │   │   ├── App.js
│   │   │   ├── App.test.js
│   │   │   ├── index.css
│   │   │   ├── index.js
│   │   │   ├── logo.svg
│   │   │   ├── reportWebVitals.js
│   │   │   ├── setupTests.js
│   │   │   ├── components/
│   │   │       ├── DatabaseView.css
│   │   │       ├── DatabaseView.js
│   │   │       ├── GenerateCombinations.css
│   │   │       ├── GenerateCombinations.js
│   │   │       ├── UpdateDatabase.js
```

Essa estrutura reflete a separação clara entre o back-end e o front-end, com o front-end consolidado no diretório `frontend/`. Certifique-se de ajustar os caminhos no código, se necessário.

## Funcionalidades

1. **Consumo de Dados da API**:
   - O script `fetch_lotofacil_data.py` consome dados da API pública da Lotofácil e armazena no banco de dados SQLite.

2. **Configuração do Banco de Dados**:
   - O script `setup_database.py` cria as tabelas necessárias para armazenar os resultados da Lotofácil e suas premiações.

3. **Análise e Geração de Combinações**:
   - O script `analyze_and_generate_combinations.py` realiza análises estatísticas dos resultados históricos e utiliza a API da OpenAI para sugerir combinações de apostas.

4. **Relatório de Acertos**:
   - O script `generate_accuracy_report.py` verifica a quantidade de acertos de combinações fornecidas em relação aos resultados históricos e gera um arquivo Excel com os dados.

## Funcionalidades do Front-End

O front-end foi desenvolvido para facilitar a interação com os dados e funcionalidades do projeto. Ele inclui:

1. **Exibição da Base de Dados**:
   - Uma tabela interativa que exibe os dados históricos da Lotofácil armazenados no banco de dados.
   - Suporte para paginação, permitindo escolher o número de itens por página.
   - Ordenação clicando no cabeçalho das colunas, com alternância entre ordem ascendente e descendente.
   - Filtragem por intervalo de datas para refinar os resultados exibidos.

2. **Sugestões de Apostas**:
   - Um espaço dedicado para configurar e exibir sugestões de apostas baseadas em análises estatísticas.
   - Permite definir o número de concursos anteriores a serem avaliados e a quantidade de apostas desejadas.

## Pré-requisitos

- Python 3.8 ou superior
- SQLite
- Biblioteca `dotenv` para carregar variáveis de ambiente
- Biblioteca `pandas` para manipulação de dados
- Biblioteca `openai` para integração com a API da OpenAI

## Instalação

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd gera-apostas-lotofacil
   ```

2. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # No Windows
   source .venv/bin/activate  # No Linux/Mac
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Crie e configure o arquivo `.env` com sua chave da API OpenAI:
   ```env
   OPENAI_API_KEY=insira_sua_chave_aqui
   ```

## Instalação do Front-End

1. Navegue até o diretório do front-end:
   ```bash
   cd frontend
   ```

2. Instale as dependências:
   ```bash
   npm install
   ```

3. Inicie o servidor de desenvolvimento:
   ```bash
   npm start
   ```

O front-end estará disponível em `http://localhost:3000`.

## Uso

### 1. Configurar o Banco de Dados
Execute o script para criar as tabelas no banco de dados:
```bash
python backend/database/setup_database.py
```

### 2. Consumir Dados da API
Obtenha os dados mais recentes da Lotofácil:
```bash
python backend/api/fetch_lotofacil_data.py
```

### 3. Analisar Dados e Gerar Combinações
Realize análises e gere combinações de apostas:
```bash
python backend/scripts/analyze_and_generate_combinations.py
```

### 4. Gerar Relatório de Acertos
Verifique os acertos de combinações fornecidas:
```bash
python backend/scripts/generate_accuracy_report.py
```

## Uso do Front-End

- **Atualizar Base de Dados**: Atualize os dados históricos diretamente pelo front-end.
- **Exibir Dados**: Visualize os dados em uma tabela interativa com suporte para paginação, ordenação e filtragem.
- **Gerar Sugestões de Apostas**: Configure os parâmetros e visualize as apostas sugeridas diretamente na interface.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).