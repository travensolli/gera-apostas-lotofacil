import sqlite3
import openai
import json
import os
from collections import Counter, defaultdict
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List

class Aposta(BaseModel):
    dezenas: List[int] = Field(..., min_length=15, max_length=15)

    @field_validator("dezenas")
    @classmethod
    def validar_dezenas(cls, v):
        if sorted(v) != v:
            raise ValueError("A lista de dezenas deve estar em ordem crescente.")
        if len(set(v)) != 15:
            raise ValueError("Dezenas não podem se repetir.")
        if any(d < 1 or d > 25 for d in v):
            raise ValueError("As dezenas devem estar entre 1 e 25.")
        return v

class ApostasModel(BaseModel):
    apostas: List[Aposta]


# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def connect_to_database():
    """Conecta ao banco de dados da Lotofácil."""
    db_path = os.path.join(os.path.dirname(__file__), "../database/lotofacil.db")
    return sqlite3.connect(db_path)

def fetch_recent_results(cursor, num_concursos):
    """Busca os resultados dos últimos num_concursos concursos."""
    cursor.execute("""
        SELECT concurso, acumulou, Dezena1, Dezena2, Dezena3, Dezena4, Dezena5, 
               Dezena6, Dezena7, Dezena8, Dezena9, Dezena10, Dezena11, Dezena12, 
               Dezena13, Dezena14, Dezena15
        FROM resultados
        ORDER BY concurso DESC
        LIMIT ?
    """, (num_concursos,))
    return cursor.fetchall()

def analyze_frequencies(results):
    """Calcula a frequência de cada dezena nos resultados."""
    all_dezenas = [dezena for result in results for dezena in result[2:]]
    return sorted(Counter(all_dezenas).items(), key=lambda x: x[1], reverse=True)

def analyze_pares_impares(results):
    """Conta a quantidade total de números pares e ímpares nos resultados."""
    pares = sum(1 for result in results for dezena in result[2:] if int(dezena) % 2 == 0)
    impares = sum(1 for result in results for dezena in result[2:] if int(dezena) % 2 != 0)
    return {"pares": pares, "impares": impares}

def analyze_consecutivos(results):
    """Analisa e conta a frequência de cada sequência consecutiva específica nos resultados."""
    sequencias_frequencia = defaultdict(int)  # Dicionário para armazenar a frequência de cada sequência

    for result in results:
        dezenas = sorted(map(int, result[2:]))  # Ordena as dezenas do resultado
        todas_sequencias = []  # Lista para armazenar todas as sequências consecutivas deste resultado

        # Identifica sequências consecutivas
        sequencia_atual = [dezenas[0]]
        for i in range(1, len(dezenas)):
            if dezenas[i] == dezenas[i - 1] + 1:
                sequencia_atual.append(dezenas[i])
            else:
                if len(sequencia_atual) >= 2:  # Só consideramos sequências de 2 ou mais
                    todas_sequencias.append(sequencia_atual)
                sequencia_atual = [dezenas[i]]
        if len(sequencia_atual) >= 2:  # Adiciona a última sequência, se aplicável
            todas_sequencias.append(sequencia_atual)

        # Gera todas as subsequências possíveis de tamanho 2 até 15
        for sequencia in todas_sequencias:
            for tamanho in range(2, len(sequencia) + 1):
                for inicio in range(len(sequencia) - tamanho + 1):
                    sub_sequencia = sequencia[inicio:inicio + tamanho]
                    # Converte a subsequência em uma string para usar como chave
                    chave = ",".join(f"{x:02d}" for x in sub_sequencia)
                    sequencias_frequencia[chave] += 1

    return dict(sequencias_frequencia)

def analyze_classificacoes(results, classificacoes):
    """Conta a frequência de cada classificação nos resultados."""
    classificacao_contagem = {key: 0 for key in classificacoes.keys()}
    for result in results:
        dezenas = list(map(int, result[2:]))
        for key, valores in classificacoes.items():
            classificacao_contagem[key] += sum(1 for dezena in dezenas if dezena in valores)
    return classificacao_contagem

def analyze_data(num_concursos):
    """Analisa os dados dos últimos num_concursos concursos da Lotofácil."""
    if not isinstance(num_concursos, int) or num_concursos <= 0:
        raise ValueError("num_concursos deve ser um inteiro positivo")

    with connect_to_database() as connection:
        cursor = connection.cursor()
        results = fetch_recent_results(cursor, num_concursos)

    # Definição das classificações
    classificacoes = {
        "PP-B-P-F": [2],
        "PP-B-NP-NF": [4, 6, 20, 22, 24],
        "PP-M-NP-F": [8],
        "PI-B-P-F": [3, 5],
        "PI-B-P-NF": [23],
        "PI-B-NP-F": [1, 21],
        "PI-B-NP-NF": [25],
        "PI-M-P-NF": [7],
        "PI-M-NP-NF": [9],
        "IP-B-NP-NF": [10, 16],
        "IP-M-NP-NF": [12, 14, 18],
        "II-B-P-NF": [11],
        "II-B-NP-NF": [15],
        "II-M-P-F": [13],
        "II-M-P-NF": [17, 19],
    }

    analise = {
        "frequencias": analyze_frequencies(results),
        "pares_impares": analyze_pares_impares(results),
        "consecutivos": analyze_consecutivos(results),
        "classificacoes": analyze_classificacoes(results, classificacoes)
    }

    return classificacoes, analise

def generate_combinations(classificacoes, analise, quantidade):
    """Gera um prompt para a API da OpenAI sugerir combinações de apostas."""
    if not isinstance(quantidade, int) or quantidade <= 0:
        raise ValueError("quantidade deve ser um inteiro positivo")

    prompt = (
        f"""
        Você é um especialista em análise estatística de loterias, com foco na Lotofácil — um jogo em que 15 números são sorteados entre os números de 1 a 25.

        Sua tarefa é gerar **exatamente {quantidade} combinações únicas**, cada uma contendo **15 números inteiros distintos entre 1 e 25**, com base em análises estatísticas de concursos anteriores.
        As combinações devem ser compatíveis com a seguinte validação Python (Pydantic):

        ```python
        from pydantic import BaseModel, Field
        from typing import List

        class Aposta(BaseModel):
            dezenas: List[int] = Field(..., min_length=15, max_length=15)

            @field_validator("dezenas")
            @classmethod
            def validar_dezenas(cls, v):
                if sorted(v) != v:
                    raise ValueError("A lista de dezenas deve estar em ordem crescente.")
                if len(set(v)) != 15:
                    raise ValueError("Dezenas não podem se repetir.")
                if any(d < 1 or d > 25 for d in v):
                    raise ValueError("As dezenas devem estar entre 1 e 25.")
                return v

        class ApostasModel(BaseModel):
            apostas: List[Aposta]

        Para gerar essas combinações, você deve se basear nas seguintes análises de dados históricos da Lotofácil, extraídas de concursos anteriores:

        1. **Frequências das dezenas**:
        - Dados: {analise['frequencias']}
        - Descrição: Esta é uma lista das dezenas que mais foram sorteadas nos concursos analisados, ordenadas da mais frequente para a menos frequente. 
        Cada item da lista é uma tupla no formato (dezena, frequência), onde 'dezena' é uma string (ex.: '10') representando o número sorteado e 'frequência' é um inteiro indicando quantas vezes essa dezena apareceu. 
        Exemplo: [('10', 50), ('15', 48), ...] significa que o número 10 foi sorteado 50 vezes, o 15 foi sorteado 48 vezes, etc.
        - Instrução: Priorize as dezenas mais frequentes ao criar as combinações, mas evite usar apenas essas dezenas para garantir diversidade.

        2. **Pares e ímpares**:
        - Dados: {analise['pares_impares']}
        - Descrição: Este é um dicionário com duas chaves: 'pares' e 'impares', cada uma associada a um valor inteiro que representa a contagem total de números pares (2, 4, 6, ..., 24) e ímpares (1, 3, 5, ..., 25) sorteados nos concursos analisados. 
        Exemplo: {{'pares': 750, 'impares': 750}} indica que, no total, foram sorteados 750 números pares e 750 números ímpares.
        - Instrução: Use essa informação para equilibrar a quantidade de números pares e ímpares em cada combinação, refletindo a proporção observada ou ajustando-a conforme padrões relevantes.

        3. **Números consecutivos**:
        - Dados: {analise['consecutivos']}
        - Descrição: Este é um dicionário que mapeia sequências consecutivas específicas de números a suas frequências nos concursos analisados. 
        As chaves são strings representando sequências de dois ou mais números consecutivos, com cada número formatado com dois dígitos e separado por vírgulas (ex.: '01,02,03,04'). Os valores são inteiros indicando quantas vezes cada sequência apareceu. 
        Exemplo: {{'01,02': 50, '02,03,04': 10, '01,02,03,04': 4}} significa que a sequência [1, 2] apareceu 50 vezes, [2, 3, 4] apareceu 10 vezes, e [1, 2, 3, 4] apareceu 4 vezes nos sorteios.
        - Instrução: Use as sequências mais frequentes como inspiração para incluir números consecutivos nas combinações, priorizando aquelas com maior ocorrência (ex.: sequências com frequência mais alta). 
        Certifique-se de variar o tamanho das sequências (de 2 a 15 números, conforme disponíveis) and evite incluir apenas sequências longas ou raras para manter a diversidade.
        
        4. **Classificações**:
        - Dados: {classificacoes}
        - Descrição: Este dicionário representa a distribuição das dezenas com base em quatro critérios combinados, codificados nas chaves no formato 'PI-B-NP-F'. Cada letra ou grupo de letras na chave indica uma característica da dezena. 
        A primeira parte refere-se à paridade dos dígitos da dezena: 'PP' indica que tanto o primeiro quanto o segundo dígito são pares, 'PI' indica par no primeiro dígito e ímpar no segundo, 'IP' representa o inverso (ímpar no primeiro e par no segundo), e 'II' indica que ambos os dígitos são ímpares. 
        A segunda parte, identificada como 'B' ou 'M', representa a posição da dezena no volante da loteria, sendo 'B' para dezenas localizadas na borda e 'M' para dezenas posicionadas no miolo. 
        O terceiro critério trata da primalidade do número, onde 'P' indica que a dezena é um número primo e 'NP' que não é. 
        Por fim, o último elemento indica a presença ou não da dezena na sequência de Fibonacci, sendo 'F' para aquelas que fazem parte da sequência e 'NF' para as que não fazem.
        Dessa forma, cada chave do dicionário representa uma combinação única desses quatro atributos, e os valores associados são listas com as dezenas que se enquadram em cada uma dessas classificações.
        - Dados: {analise['classificacoes']}
        - Descrição: Este dicionário representa a frequência das dezenas com base na classificação acima.
        - Instrução: Diversifique as combinações incorporando dezenas proporcionalmente às frequências de cada classificação, evitando a concentração excessiva em uma única categoria.

        ### Regras obrigatórias:
        - Cada combinação deve conter **exatamente 15 dezenas únicas**.
        - Todos os números devem estar entre **1 e 25** (inclusive).
        - As dezenas em cada combinação devem estar em **ordem crescente**.
        O resultado deve ser apenas uma **lista de listas** no formato JSON/Python padrão, como este exemplo:

        apostas = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            [2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 25],
            ...
        ]

        **Sempre inclua a variável (`apostas =`)**
        **Não inclua comentários ou explicações**
        **O conteúdo deve começar diretamente com `[` e terminar com `]`**

        Gere agora as {quantidade} combinações de apostas no formato especificado.
        """
    )

    # Configurar a API da OpenAI
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Fazer a chamada para a API da OpenAI
    response = openai.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Você é um especialista em estatísticas de loteria e análise de dados para tomada de decisão"},
            {"role": "user", "content": prompt}
        ]
    )

    # Resposta como string (esperado: "apostas = [[...], [...]]")
    sugestoes_raw = response.choices[0].message.content
    #print(sugestoes_raw)

    # Executa apenas a linha que define `apostas`
    local_vars = {}
    try:
        exec(sugestoes_raw, {}, local_vars)
        apostas_lista = local_vars.get("apostas")
        if not isinstance(apostas_lista, list):
            raise ValueError("Formato inválido: variável 'apostas' não encontrada ou não é uma lista.")

        # Validação com Pydantic
        apostas_validadas = ApostasModel(apostas=[Aposta(dezenas=a) for a in apostas_lista])
        return apostas_validadas

    except (SyntaxError, NameError, ValidationError, ValueError) as e:
        raise RuntimeError(f"Erro ao processar sugestões da IA: {e}")

if __name__ == "__main__":
    num_concursos = int(input("Quantos concursos você deseja analisar? "))
    classificacoes,analise = analyze_data(num_concursos)
    quantidade = int(input("Quantas combinações você deseja gerar? "))
    
    # print("Resultados da Análise:\n")
    # print(f"Frequências das dezenas (top 15): {analise['frequencias'][:15]}\n")
    # print(f"Pares e ímpares: {analise['pares_impares']}\n")
    # print(f"Números consecutivos: {analise['consecutivos']}\n")
    # print(f"Classificações: {analise['classificacoes']}\n")
    # print("-------------------------\n")  # Linha em branco para separar as seções
  
    sugestoes_model = generate_combinations(classificacoes, analise, quantidade)
    for i, aposta in enumerate(sugestoes_model.apostas, start=1):
        print(f"Aposta {i}: {aposta.dezenas}")