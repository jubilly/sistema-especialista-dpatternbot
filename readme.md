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
{
"artigos": [
{
"id": 1,
"titulo": "Reserve+ App: Aplicativo para Reservas de Ambientes",
"artigo": "1.pdf"
},
{
"id": 2,
"titulo": "Uma Solução Modularizada e Plugável para Indexação de Informações sobre Trabalhos Acadêmicos escritos em Latex",
"artigo": "2.pdf"
},
{
"id": 3,
"titulo": "Uma Arquitetura para um Aplicativo de Visualização de Objetos Educacionais 3D: o caso EducaRA",
"artigo": "3.pdf"
}
]
}

<!-- objetos, command, solicitação, padrão -->
