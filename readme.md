## Qual a proposta do Chatterbot DPattern bot?

É um sistema especialista que ajuda desenvolvedores a identificar qual o melhor design pattern para um projeto de software, o DPattern Bot. O sistema irá minerar os dados de livros clássicos de padrões de desenvolvimento de software.

## Como executar o projeto:

python inicializar_nltk.py
python processar_artigos.py
python treinamento.py
python servico.py
python robo.py
python ./chat/chat.py

rodar no postman um post http://127.0.0.1:5003/padroes, body:
{ "chave1": "objetos", "chave2": "command", "chave3": "solicitação", "chave4": "padrao", "chave5": "", "chave6": "", "chave7": ""}
