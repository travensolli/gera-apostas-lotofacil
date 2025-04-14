import requests
import json
import sqlite3

def fetch_lotofacil_data():
    url = "https://loteriascaixa-api.herokuapp.com/api/lotofacil"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Salvar os dados em um arquivo JSON temporariamente
        with open("lotofacil_data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        print("Dados da Lotofácil obtidos com sucesso!")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None

def save_to_database(data):
    connection = sqlite3.connect("database/lotofacil.db")
    cursor = connection.cursor()

    # Verificar se `data` é uma lista
    if isinstance(data, list):
        for item in data:
            save_single_result(cursor, item)
    else:
        save_single_result(cursor, data)

    connection.commit()
    connection.close()
    print("Dados salvos no banco de dados com sucesso!")

def save_single_result(cursor, item):
    # Inserir dados na tabela resultados
    cursor.execute('''
        INSERT INTO resultados (
            concurso, data, local, acumulou, valorEstimadoProximoConcurso,
            Dezena1, Dezena2, Dezena3, Dezena4, Dezena5,
            Dezena6, Dezena7, Dezena8, Dezena9, Dezena10,
            Dezena11, Dezena12, Dezena13, Dezena14, Dezena15
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        item["concurso"],
        item["data"],
        item["local"],
        item["acumulou"],
        item["valorEstimadoProximoConcurso"],
        *item["dezenas"]
    ))

    # Inserir dados na tabela premiacoes
    for premiacao in item.get("premiacoes", []):
        cursor.execute('''
            INSERT INTO premiacoes (concurso, descricao, faixa, ganhadores, valorPremio)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            item["concurso"],
            premiacao["descricao"],
            premiacao["faixa"],
            premiacao["ganhadores"],
            premiacao["valorPremio"]
        ))

if __name__ == "__main__":
    data = fetch_lotofacil_data()
    if data:
        save_to_database(data)