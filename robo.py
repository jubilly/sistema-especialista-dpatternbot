from chatterbot import ChatBot
from processar_artigos import get_artigos

NOME_ROBO = "Robô Dpattern. Foco em ajudar desenvolvedores a identificar qual o melhor padrão de projeto para o desenvolvimento de um sistema."

BD_ROBO = "chat.sqlite3"

CONFIANCA_MINIMA = 0.60

CAMINHO_BD = "C:/Users/amand/OneDrive/Documentos/Pos-Graduacao/Segundo semestre/sistemas-especialistas-projetos/projeto-dpatternbot"

BD_ARTIGOS = f"{CAMINHO_BD}/artigos.sqlite3"

def inicializar():
    sucesso, robo, artigos = False, None, None

    try:
        robo = ChatBot(NOME_ROBO, read_only=True, storage_adapter="chatterbot.storage.SQLStorageAdapter", database_uri=f"sqlite:///{BD_ROBO}")
        artigos = get_artigos(como_linhas=True)

        sucesso = True
    except Exception as e:
        print(f"erro inicializando o robô: {str(e)}")

    return sucesso, robo, artigos

def pesquisar_artigos_por_chaves(chaves, artigos):
    encontrou, artigos_selecionados = False, {}

    for artigo in artigos:
        for chave in chaves:
            chave = chave.strip()

            if chave and any (chave in c for c in [artigo['chave1'], artigo['chave2'], artigo['chave3'], artigo['chave4'], artigo['chave5'], artigo['chave6'], artigo['chave7']]):
                artigos_selecionados[artigo["id"]] = {
                    "id": artigo["id"],
                    "titulo": artigo["titulo"],
                    "resumo": artigo["resumo"]
                }

                encontrou = True
    print(f"pesquisar artigos, artigo: {artigos_selecionados}")
    return encontrou, artigos_selecionados

def executar(robo):
    while True:
        mensagem = input("👤 ")
        resposta = robo.get_response(mensagem.lower())

        if resposta.confidence >= CONFIANCA_MINIMA:
            print(f"🤖 {resposta.text} [confiança = {resposta.confidence}]")
        else:
            print(f"🤖 Infelizmente, ainda não sei responder esta pergunta. Pesquiser por mais informações em fontes como o livro Padrões de Projetos - Soluções Reutilizáveis de Software Orientados a Objetos - Autor (Erich Gamma) [confiança = {resposta.confidence}]")

if __name__ == "__main__":
    sucesso, robo, _ = inicializar()
    if sucesso:
        executar(robo)