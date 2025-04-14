# Projeto Lotofácil

Este projeto foi desenvolvido para realizar análises estatísticas e gerar combinações de apostas para a Lotofácil, utilizando dados históricos e integração com a API da OpenAI.

## Estrutura do Projeto

```
lotofacil/
├── api/
│   ├── fetch_lotofacil_data.py  # Script para consumir dados da API da Lotofácil
├── database/
│   ├── lotofacil.db             # Banco de dados SQLite com os resultados históricos
│   ├── setup_database.py        # Script para configurar o banco de dados
├── scripts/
│   ├── analyze_and_generate_combinations.py  # Análise e geração de combinações com OpenAI
│   ├── generate_accuracy_report.py           # Geração de relatório de acertos
├── .env                         # Arquivo para armazenar variáveis de ambiente (ex.: chave da API OpenAI)
├── requirements.txt             # Dependências do projeto
└── README.md                    # Documentação do projeto
```

## Funcionalidades

1. **Consumo de Dados da API**:
   - O script `fetch_lotofacil_data.py` consome dados da API pública da Lotofácil e armazena no banco de dados SQLite.

2. **Configuração do Banco de Dados**:
   - O script `setup_database.py` cria as tabelas necessárias para armazenar os resultados da Lotofácil e suas premiações.

3. **Análise e Geração de Combinações**:
   - O script `analyze_and_generate_combinations.py` realiza análises estatísticas dos resultados históricos e utiliza a API da OpenAI para sugerir combinações de apostas.

4. **Relatório de Acertos**:
   - O script `generate_accuracy_report.py` verifica a quantidade de acertos de combinações fornecidas em relação aos resultados históricos e gera um arquivo Excel com os dados.

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
   cd lotofacil
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

## Uso

### 1. Configurar o Banco de Dados
Execute o script para criar as tabelas no banco de dados:
```bash
python database/setup_database.py
```

### 2. Consumir Dados da API
Obtenha os dados mais recentes da Lotofácil:
```bash
python api/fetch_lotofacil_data.py
```

### 3. Analisar Dados e Gerar Combinações
Realize análises e gere combinações de apostas:
```bash
python scripts/analyze_and_generate_combinations.py
```

### 4. Gerar Relatório de Acertos
Verifique os acertos de combinações fornecidas:
```bash
python scripts/generate_accuracy_report.py
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).