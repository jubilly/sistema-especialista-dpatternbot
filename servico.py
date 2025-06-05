from flask import Flask, Response, request
from robo import *

import json

sucesso, robo, artigos = inicializar()
servico = Flask(NOME_ROBO)

INFO = {
    "descricao": "Robô Dpattern. Foco em ajudar desenvolvedores a identificar qual o melhor padrão de projeto para o desenvolvimento de um sistema.",
    "versao": "1.0"
}

@servico.get("/")
def get_info():
    return Response(json.dumps(INFO), status=200, mimetype="application/json")

@servico.get("/alive")
def is_alive():
    return Response(json.dumps({"alive": "sim" if sucesso else "não"}), status=200, mimetype="application/json")

@servico.post("/responder")
def get_resposta():
    if sucesso:
        conteudo = request.json
        resposta = robo.get_response(conteudo["pergunta"])

        print(f"pesquisa front", conteudo)
        print(f"resposta robo", resposta)

        return Response(json.dumps({"resposta": resposta.text, "confianca": resposta.confidence}), status=200, mimetype="application/json")
    else:
        return Response(status=503)
    
@servico.post("/artigos")
def get_artigos():
    conteudo = request.json
    chaves = [conteudo['chave1'], conteudo['chave2'], conteudo['chave3'], conteudo['chave4'], conteudo['chave5'], conteudo['chave6'], conteudo['chave7']]

    encontrou, artigos_selecionados = pesquisar_artigos_por_chaves(chaves, artigos)

    return Response(json.dumps({"artigos": list(artigos_selecionados.values())}), status=200 if encontrou else 204, mimetype="application/json")


if __name__ == "__main__":
    servico.run(host="0.0.0.0", port=5003, debug=True)