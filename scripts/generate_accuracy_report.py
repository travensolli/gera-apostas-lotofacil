import sqlite3
import pandas as pd
import os


# Conectar ao banco de dados
db_path = os.path.join(os.path.dirname(__file__), "../database/lotofacil.db")
conn = sqlite3.connect(db_path)

# Carregar a tabela resultados para um DataFrame
query = "SELECT * FROM resultados ORDER BY concurso DESC"
df = pd.read_sql_query(query, conn)

# Função para verificar acertos de uma aposta
def verificar_acertos(aposta, resultados):
    acertos = []
    for resultado in resultados:
        # Converter dezenas de texto para inteiros
        resultado = [int(dezena) for dezena in resultado]
        num_acertos = len(set(aposta) & set(resultado))
        acertos.append(num_acertos)
    return acertos

# Iterar sobre cada conjunto de dezenas dos concursos
resultados_anteriores = df[[f"Dezena{i}" for i in range(1, 16)]].values.tolist()
apostas = [[1, 3, 4, 5, 6, 9, 13, 14, 15, 19, 20, 21, 22, 24, 25],
    [1, 2, 3, 8, 9, 10, 11, 13, 14, 16, 18, 20, 22, 24, 25],
    [2, 3, 5, 8, 10, 11, 12, 13, 14, 15, 18, 20, 21, 22, 23],
    [1, 2, 7, 8, 9, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24],
    [1, 3, 4, 8, 9, 10, 11, 14, 16, 17, 18, 20, 22, 23, 25]

]

acertos_dict = {}
for idx, aposta_especifica in enumerate(apostas):
    coluna_acertos = f"Aposta_{idx}"
    acertos_dict[coluna_acertos] = verificar_acertos(aposta_especifica, resultados_anteriores)

# Concatenar todas as colunas de acertos ao DataFrame original
acertos_df = pd.DataFrame(acertos_dict)
df = pd.concat([df, acertos_df], axis=1)
df['data'] = pd.to_datetime(df['data'], dayfirst=True)

# Converter as dezenas para inteiros antes de salvar no Excel
df[[f"Dezena{i}" for i in range(1, 16)]] = df[[f"Dezena{i}" for i in range(1, 16)]].astype(int)

# Salvar o DataFrame em um arquivo Excel
df.to_excel('acertos_minhas_apostas.xlsx', index=False)

print("\nArquivo Excel 'acertos_minhas_apostas.xlsx' gerado com sucesso.")