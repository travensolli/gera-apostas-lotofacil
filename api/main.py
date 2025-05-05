from fastapi import FastAPI
from scripts.analyze_and_generate_combinations import analyze_data, generate_combinations
from api.fetch_lotofacil_data import fetch_lotofacil_data, save_to_database
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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