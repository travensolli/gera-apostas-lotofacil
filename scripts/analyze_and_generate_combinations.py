import sqlite3
import openai
import json
import os
from collections import Counter, defaultdict
from dotenv import load_dotenv

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

    return analise

def generate_combinations(analise, quantidade):
    """Gera um prompt para a API da OpenAI sugerir combinações de apostas."""
    if not isinstance(quantidade, int) or quantidade <= 0:
        raise ValueError("quantidade deve ser um inteiro positivo")

    prompt = (
        f"""
        Você é um especialista em análise estatística de loterias, com foco na Lotofácil, um jogo em que são sorteados 15 números dentre 25 possíveis (de 1 a 25). 
        Sua tarefa é sugerir {quantidade} combinações de 15 dezenas para apostar no próximo concurso, utilizando dados históricos e análises estatísticas como base. 
        Cada combinação deve ser uma lista única contendo exatamente 15 números inteiros entre 1 e 25, sem repetições, ordenados em ordem crescente e formatados entre colchetes, com os números separados por vírgulas. 
        Por exemplo: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15].

        Para gerar essas combinações, você deve se basear nas seguintes análises de dados históricos da Lotofácil, extraídas de concursos anteriores:

        1. **Frequências das dezenas (top 15)**:
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
        - Dados: {analise['classificacoes']}
        - Descrição: Este é um dicionário onde as chaves são strings representando categorias ou padrões predefinidos das dezenas (ex.: 'PP-B-P-F'), e os valores são inteiros indicando quantas vezes as dezenas dessas categorias apareceram. 
        O significado exato das siglas não é fornecido, mas presume-se que sejam critérios como posição, frequência ou outros atributos estatísticos.
        - Instrução: Diversifique as combinações incorporando dezenas de diferentes classificações, proporcionalmente às suas contagens, para explorar padrões variados.

        **Objetivo**: Gere {quantidade} combinações que maximizem as chances de sucesso no próximo concurso, considerando as análises fornecidas. Certifique-se de que:
        - Cada combinação tenha exatamente 15 números únicos.
        - Todos os números estejam entre 1 e 25.
        - As combinações sejam distintas entre si.
        - Os números em cada combinação estejam em ordem crescente e no formato especificado.

        """
    )

    # Configurar a API da OpenAI
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Fazer a chamada para a API da OpenAI
    response = openai.chat.completions.create(
        model="gpt-4.5-preview",
        messages=[
            {"role": "system", "content": "Você é um especialista em estatísticas de loteria e análise de dados para tomada de decisão"},
            {"role": "user", "content": prompt}
        ]
    )

    # Retornar as combinações sugeridas
    return response.choices[0].message.content

if __name__ == "__main__":
    num_concursos = int(input("Quantos concursos você deseja analisar? "))
    analise = analyze_data(num_concursos)
    quantidade = int(input("Quantas combinações você deseja gerar? "))
    
    print("Resultados da Análise:\n")
    print(f"Frequências das dezenas (top 15): {analise['frequencias'][:15]}\n")
    print(f"Pares e ímpares: {analise['pares_impares']}\n")
    print(f"Números consecutivos: {analise['consecutivos']}\n")
    print(f"Classificações: {analise['classificacoes']}\n")
    print("-------------------------\n")  # Linha em branco para separar as seções
  
    sugestoes = generate_combinations(analise, quantidade)
    print("Sugestões de combinações:")
    print(sugestoes)