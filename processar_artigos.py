import json
import sqlite3
import os
from nltk import word_tokenize, corpus
from nltk.corpus import floresta
from collections import Counter
from string import punctuation

# Caminhos
CAMINHO_JSON = "C:\\Users\\amand\\OneDrive\\Documentos\\Pos-Graduacao\\Segundo semestre\\sistemas-especialistas-projetos\\projeto-dpatternbot\\fontes\\design-patterns.json"
CAMINHO_BD = "C:\\Users\\amand\\OneDrive\\Documentos\\Pos-Graduacao\\Segundo semestre\\sistemas-especialistas-projetos\\projeto-dpatternbot"
BD_ARTIGOS = f"{CAMINHO_BD}/artigos.sqlite3"
PALAVRAS_CHAVE_POR_ARTIGO = 7
FREQUENCIA_MINIMA = 2

CLASSES_GRAMATICAIS_INDESEJADAS = ["adv", "v-inf", "v-fin", "v-pcp", "v-ger", "num", "adj"]

def inicializar():
    palavras_de_parada = set(corpus.stopwords.words("portuguese"))

    classificacoes = {}
    for (palavra, classificacao) in floresta.tagged_words():
        classificacoes[palavra.lower()] = classificacao

    return palavras_de_parada, classificacoes

def eliminar_palavras_de_parada(tokens, palavras_de_parada):
    tokens_filtrados = []

    for token in tokens:
        if token not in palavras_de_parada:
            tokens_filtrados.append(token)

    return tokens_filtrados

def eliminar_pontuacoes(tokens):
    tokens_filtrados = []

    for token in tokens:
        if token not in punctuation:
            tokens_filtrados.append(token)

    return tokens_filtrados

def eliminar_classes_gramaticais(tokens, classificacoes):
    tokens_filtrados = []

    for token in tokens:
        if token in classificacoes.keys():
            classificacao = classificacoes[token]
            if not any (s in classificacao for s in CLASSES_GRAMATICAIS_INDESEJADAS):
                tokens_filtrados.append(token)
        else:
            tokens_filtrados.append(token)

    return tokens_filtrados

def eliminar_frequencias_baixas(tokens):
    tokens_filtrados, frequencias = [], Counter(tokens)

    # print(f"tokens enviados: {tokens}")

    for token, frequencia in frequencias.most_common():

        # print(f"a frequencia: {frequencia}")
        
        if frequencia >= FREQUENCIA_MINIMA:
            tokens_filtrados.append(token)

    return tokens_filtrados

def iniciar_banco_artigos():
    if os.path.exists(BD_ARTIGOS):
        os.remove(BD_ARTIGOS)

    conexao = sqlite3.connect(BD_ARTIGOS)
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS artigos(id INTEGER, titulo TEXT, resumo TEXT)")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chaves(
            id_artigo INTEGER,
            chave1 TEXT, chave2 TEXT, chave3 TEXT,
            chave4 TEXT, chave5 TEXT, chave6 TEXT, chave7 TEXT
        )
    """)
    conexao.close()

def gravar_artigo(id_artigo, titulo, chaves, resumo):
    conexao = sqlite3.connect(BD_ARTIGOS)
    cursor = conexao.cursor()

    insert = f"INSERT INTO artigos(id, titulo, resumo) VALUES({id_artigo}, '{titulo}', '{resumo}')"
    cursor.execute(insert)

    while len(chaves) < PALAVRAS_CHAVE_POR_ARTIGO:
        chaves.append("")

    insert = f"INSERT INTO chaves(id_artigo, chave1, chave2, chave3, chave4, chave5, chave6, chave7) VALUES ({id_artigo}"
    for contador, chave in enumerate(chaves):
        insert += f", '{chave}'"

        if contador + 1 == PALAVRAS_CHAVE_POR_ARTIGO:
            break
    insert += ")"
    cursor.execute(insert)

    conexao.commit()
    conexao.close()

def get_artigos(como_linhas = False):
    conexao = sqlite3.connect(BD_ARTIGOS)
    if como_linhas:
        conexao.row_factory = sqlite3.Row

    cursor = conexao.cursor()
    cursor.execute("SELECT id, titulo, resumo, chave1, chave2, chave3, chave4, chave5, chave6, chave7 FROM artigos, chaves WHERE chaves.id_artigo = artigos.id")
    artigos = cursor.fetchall()
    conexao.close()

    # print(f"artigos {artigos}")

    return artigos

if __name__ == "__main__":
    palavras_de_parada, classificacoes = inicializar()
    iniciar_banco_artigos()

    with open(CAMINHO_JSON, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

        for item in dados:
            id_artigo = item["id"]
            titulo = item["titulo"]
            resumo = item["resumo"]

            tokens = word_tokenize(resumo.lower())

            # print(f"1. word_tokenize id_artigo: {id_artigo}, tokens {tokens}")

            tokens = eliminar_palavras_de_parada(tokens, palavras_de_parada)
            # print(f"2. palavras de parada id_artigo: {id_artigo}, tokens {tokens}")
            tokens = eliminar_pontuacoes(tokens)
            # print(f"3. eliminar_pontuacoes id_artigo: {id_artigo}, tokens {tokens}")
            tokens = eliminar_classes_gramaticais(tokens, classificacoes)
            # print(f"3. eliminar_classes_gramaticais id_artigo: {id_artigo}, tokens {tokens}")

            tokens = eliminar_frequencias_baixas(tokens)

            print(f"4. eliminar_frequencias_baixas id_artigo: {id_artigo}, tokens {tokens}")


            # print(f"id_artigo: {id_artigo}, titulo: {titulo}, tokens: {tokens}, resum: {resumo}")

            gravar_artigo(id_artigo, titulo, tokens, resumo)

    # print("Padrões processados com sucesso.")

    artigos = get_artigos()

    # print(f"artigos: {artigos}")