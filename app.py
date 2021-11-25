from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy

from flask_marshmallow import Marshmallow

import os

app = Flask(__name__)

# Diretório base
basedir = os.path.abspath(os.path.dirname(__file__))

# Banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa banco de dados
db = SQLAlchemy(app)

ma = Marshmallow(app)



# Produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True)
    descricao = db.Column(db.String(200))
    preco = db.Column(db.Float)
    quantidade = db.Column(db.Integer)

    def __init__(self, nome, descricao, preco, quantidade):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.quantidade = quantidade


class ProdutoSchema(ma.Schema):

    class Meta:
        fields = ('id', 'nome', 'descricao', 'preco', 'quantidade')

produto_schema = ProdutoSchema()
produtos_schema = ProdutoSchema(many=True) 



# Criar um produto
@app.route('/produto', methods=['POST'])
def criar_produto():

    nome = request.json['nome']
    descricao = request.json['descricao']
    preco = request.json['preco']
    quantidade = request.json['quantidade']


    novo_produto = Produto(nome, descricao, preco, quantidade)

    db.session.add(novo_produto)
    db.session.commit()

    return produto_schema.jsonify(novo_produto)


# Selecionar todos os produtos
@app.route('/produto', methods=['GET'])
def selecionar_produtos():

    todos_produtos = Produto.query.all()

    resultado = produtos_schema.dump(todos_produtos)

    return jsonify(resultado)


# Selecionar um produtos
@app.route('/produto/<id>', methods=['GET'])
def selecionar_produto(id):

    produto = Produto.query.get(id)

    return produto_schema.jsonify(produto)



# Atualizar produto
@app.route('/produto/<id>', methods=['PUT'])
def atualizar_produto(id):

    produto = Produto.query.get(id)

    nome = request.json['nome']
    descricao = request.json['descricao']
    preco = request.json['preco']
    quantidade = request.json['quantidade']

    produto.nome = nome
    produto.descricao = descricao
    produto.preco = preco
    produto.quantidade = quantidade
 
    db.session.commit()

    return produto_schema.jsonify(produto)


# Selecionar um produtos
@app.route('/produto/<id>', methods=['DELETE'])
def apagar_produto(id):

    produto = Produto.query.get(id)

    db.session.delete(produto)

    db.session.commit()

    return produto_schema.jsonify(produto)




if __name__ == '__main__':
    app.run(debug=True)