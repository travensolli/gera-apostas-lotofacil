from fastapi import FastAPI, Query
from scripts.analyze_and_generate_combinations import analyze_data, generate_combinations
from api.fetch_lotofacil_data import fetch_lotofacil_data, save_to_database
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from typing import Optional
import os

class GenerateCombinationsRequest(BaseModel):
    num_concursos: int
    quantidade: int

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens (ou especifique o domínio do frontend)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

@app.post("/update-database")
def update_database():
    try:
        data = fetch_lotofacil_data()
        if data:
            save_to_database(data)
            return {"message": "Base de dados atualizada com sucesso!"}
        return {"error": "Erro ao buscar dados da API"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/generate-combinations")
def generate_combinations_endpoint(request: GenerateCombinationsRequest):
    try:
        classificacoes, analise = analyze_data(request.num_concursos)
        combinations = generate_combinations(classificacoes, analise, request.quantidade)
        for i, aposta in enumerate(combinations.apostas, start=1):
            print(f"Aposta {i}: {aposta.dezenas}")
        return {"combinations": combinations}
    except Exception as e:
        return {"error": str(e)}

@app.get("/get-database-data")
def get_database_data(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    order_by: Optional[str] = Query("concurso"),
    filter_date: Optional[str] = None
):
    try:
        # Construir o caminho do banco de dados de forma genérica
        db_path = os.path.join(os.path.dirname(__file__), "../database/lotofacil.db")
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Construir consulta SQL com paginação, ordenação e filtragem
        query = "SELECT * FROM resultados"
        params = []

        if filter_date:
            query += " WHERE data = ?"
            params.append(filter_date)

        query += f" ORDER BY {order_by} LIMIT ? OFFSET ?"
        params.extend([page_size, (page - 1) * page_size])

        cursor.execute(query, params)
        rows = cursor.fetchall()

        # Obter os nomes das colunas
        column_names = [description[0] for description in cursor.description]

        # Formatar os dados como uma lista de dicionários
        data = [dict(zip(column_names, row)) for row in rows]

        # Fechar a conexão
        connection.close()

        return {"data": data}
    except Exception as e:
        return {"error": str(e)}