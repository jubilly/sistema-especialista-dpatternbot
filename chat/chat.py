from flask import Flask, render_template, Response, request, session, send_from_directory
import requests
import json
import os
import secrets

URL_ROBO = "http://localhost:5003"
URL_ROBO_ALIVE = f"{URL_ROBO}/alive"
URL_ROBO_RESPONDER = f"{URL_ROBO}/responder"
URL_ROBO_PESQUISAR_ARTIGOS = f"{URL_ROBO}/padroes"

CONFIANCA_MINIMA = 0.60
CAMINHO_ARQUIVOS = "C:\\Users\\amand\\OneDrive\\Documentos\\Pos-Graduacao\\Segundo semestre\\sistemas-especialistas\\projeto-dpatternbot\\chat\\static\\arquivos"

chat = Flask(__name__)
chat.secret_key = secrets.token_hex(16)

def acessar_robo(url, para_enviar = None):
    sucesso, resposta = False, None    

    try:
        if para_enviar:
            resposta = requests.post(url, json=para_enviar)
        else:
            resposta = requests.get(url)
        
        resposta = resposta.json()

        sucesso = True
    except Exception as e:
        print(f"erro acessando back-end: {str(e)}")

    return sucesso, resposta

def robo_alive():
    sucesso, resposta = acessar_robo(URL_ROBO_ALIVE)

    return sucesso and resposta["alive"] == "sim"

def verificar_modo_de_pesquisa(resposta_robo):
    return "Informe as palavras-chave que deseja pesquisar" in resposta_robo

def perguntar_robo(pergunta):
    sucesso, resposta = acessar_robo(URL_ROBO_RESPONDER, {"pergunta": pergunta})
    em_modo_de_pesquisa = False

    mensagem = f"🤖 Infelizmente, ainda não sei responder esta pergunta. Pesquiser por mais informações em fontes como o livro Padrões de Projetos - Soluções Reutilizáveis de Software Orientados a Objetos - Autores: Erich Gamma, Richard Helm, Ralph Johnson, John Vlissid"

    if sucesso and resposta["confianca"] >= CONFIANCA_MINIMA:
            mensagem = resposta["resposta"]
            em_modo_de_pesquisa = verificar_modo_de_pesquisa(mensagem)

    return mensagem, em_modo_de_pesquisa

def pesquisar_artigos(chaves):
    artigos_selecionados = []

    sucesso, resposta = acessar_robo(URL_ROBO_PESQUISAR_ARTIGOS, {"chave1": chaves[0], "chave2": chaves[1],"chave3": chaves[2],"chave4": chaves[3],"chave5": chaves[4],"chave6": chaves[5],"chave7": chaves[6]})

    if sucesso:
        artigos = resposta["artigos"]
        ordem = 1
        for artigo in artigos:
            artigos_selecionados.append({"id": artigo["id"], "titulo": f"{ordem} - {artigo['titulo']}", "resumo": f"{artigo['resumo']}"})

            ordem += 1
    
    return artigos_selecionados

@chat.get("/")
def index():
    return render_template("index.html")

@chat.post("/responder")
def get_resposta():
    resposta, artigos = "", []

    conteudo = request.json
    pergunta = conteudo["pergunta"]

    pesquisar_por_artigos = "em_modo_de_pesquisa" in session.keys() and session["em_modo_de_pesquisa"]


    if pesquisar_por_artigos:
        session["em_modo_de_pesquisa"] = False

        chaves = pergunta.split(",")

        while len(chaves) < 7:
            chaves.append("")
        artigos = pesquisar_artigos(chaves)
        if len(artigos):
            resposta = "Caso deseje refazer a pesquisa, digite 'pesquisar de novo' ou pressione os botões."
        else:
            resposta = "Não encontrei padrões de projeto de software que correspondem a sua busca. Tente de novo com outros parâmetros de pesquisa"
    else:
        resposta, em_modo_de_pesquisa = perguntar_robo(pergunta)

        if em_modo_de_pesquisa:
            session["em_modo_de_pesquisa"] = True
    session["artigos_selecionados"] = artigos

    return Response(json.dumps({"resposta": resposta, "artigos": artigos, "artigos_pesquisados": pesquisar_por_artigos}), status=200, mimetype="application/json")

if __name__ == "__main__":
    chat.run(
        host = "0.0.0.0",
        port = 5004,
        debug=True
    )
