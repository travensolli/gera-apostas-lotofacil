import sqlite3

def setup_database():
    # Conectar ao banco de dados SQLite
    connection = sqlite3.connect("database/lotofacil.db")
    cursor = connection.cursor()

    # Criar tabela para armazenar os resultados da Lotofácil
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resultados (
            concurso INTEGER PRIMARY KEY,
            data TEXT NOT NULL,
            local TEXT,
            acumulou BOOLEAN,
            valorEstimadoProximoConcurso REAL,
            Dezena1 TEXT,
            Dezena2 TEXT,
            Dezena3 TEXT,
            Dezena4 TEXT,
            Dezena5 TEXT,
            Dezena6 TEXT,
            Dezena7 TEXT,
            Dezena8 TEXT,
            Dezena9 TEXT,
            Dezena10 TEXT,
            Dezena11 TEXT,
            Dezena12 TEXT,
            Dezena13 TEXT,
            Dezena14 TEXT,
            Dezena15 TEXT
        )
    ''')

    # Criar tabela para armazenar as premiações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS premiacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concurso INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            faixa INTEGER NOT NULL,
            ganhadores INTEGER NOT NULL,
            valorPremio REAL NOT NULL,
            FOREIGN KEY (concurso) REFERENCES resultados (concurso)
        )
    ''')

    print("Banco de dados configurado com sucesso!")

    # Fechar conexão
    connection.commit()
    connection.close()

if __name__ == "__main__":
    setup_database()