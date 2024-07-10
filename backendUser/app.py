from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
import requests

app = Flask(__name__)

app.config['SWAGGER'] = {
    "info": {
        "title": "Api Controller",
        "description": "API para controlar o acesso de outras apis",
        "contact": {
            "responsibleDeveloper": "Bento",
            "email": "sbento.ti@gmail.com",
            "url": "https://senhorbento.com.br/",
        },
        "version": "1.0"
    },
    "operationId": "getmyData",
    "consumes": [
        "application/json"
    ],
    "produces": [
        "application/json"
    ]
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
swagger = Swagger(app)

_URL_BASE_ = 'http://backendexternal:5001/'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    access_level = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

def get_access_level_by_id(user_id):
    user = User.query.get_or_404(user_id)
    return user.access_level

@app.route('/users', methods=['POST'])
def add_user():
    """
    Criar um novo usuário
    ---
    parameters:
        - name: body
          in: body
          required: True
          schema:
            type: object
            required:
                - login
                - password
                - access_level
            properties:
                login:
                    type: string
                    example: "user1"
                password:
                    type: string
                    example: "pass123"
                access_level:
                    type: integer
                    example: 1
    responses:
        201:
            description: Usuário criado com sucesso
        400:
            description: Erro na requisição
    """
    data = request.get_json()
    new_user = User(
        login=data['login'], password=data['password'], access_level=data['access_level'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuário criado com sucesso'}), 201

@app.route('/users', methods=['GET'])
def get_users():
    """
    Obter todos os usuários
    ---
    responses:
        200:
            description: Lista de usuários
            schema:
                type: array
                items:
                    type: object
                    properties:
                        id:
                            type: integer
                            example: 1
                        login:
                            type: string
                            example: "user1"
                        password:
                            type: string
                            example: "pass123"
                        access_level:
                            type: integer
                            example: 1
    """
    users = User.query.all()
    output = []
    for user in users:
        user_data = {'id': user.id, 'login': user.login,
                     'password': user.password, 'access_level': user.access_level}
        output.append(user_data)
    return jsonify(output), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Obter um usuário específico por ID
    ---
    parameters:
        - name: user_id
          in: path
          type: integer
          required: True
          description: ID do usuário
    responses:
        200:
            description: Detalhes do usuário
            schema:
                type: object
                properties:
                    id:
                        type: integer
                        example: 1
                    login:
                        type: string
                        example: "user1"
                    password:
                        type: string
                        example: "pass123"
                    access_level:
                        type: integer
                        example: 1
        404:
            description: Usuário não encontrado
    """
    user = User.query.get_or_404(user_id)
    user_data = {'id': user.id, 'login': user.login,
                 'password': user.password, 'access_level': user.access_level}
    return jsonify(user_data), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Atualizar um usuário existente
    ---
    parameters:
        - name: user_id
          in: path
          type: integer
          required: True
          description: ID do usuário
        - name: body
          in: body
          required: True
          schema:
            type: object
            required:
                - login
                - password
                - access_level
            properties:
                login:
                    type: string
                    example: "user1"
                password:
                    type: string
                    example: "pass123"
                access_level:
                    type: integer
                    example: 1
    responses:
        200:
            description: Usuário atualizado com sucesso
        400:
            description: Erro na requisição
        404:
            description: Usuário não encontrado
    """
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    user.login = data['login']
    user.password = data['password']
    user.access_level = data['access_level']
    db.session.commit()
    return jsonify({'message': 'Usuário atualizado com sucesso'}), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Excluir um usuário existente
    ---
    parameters:
        - name: user_id
          in: path
          type: integer
          required: True
          description: ID do usuário
    responses:
        200:
            description: Usuário excluído com sucesso
        404:
            description: Usuário não encontrado
    """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Usuário excluído com sucesso'}), 200

@app.route('/external/posts/<int:user_id>', methods=['GET'])
def get_posts(user_id):
    """
    Obter todos os posts, desde que o user tenha acesso.
    Necessário acesso de nível 3 ou maior.
    ---
    parameters:
        - name: user_id
          in: path
          type: integer
          required: true
          description: ID do usuario
    responses:
        200:
            description: Lista de posts
            schema:
                type: array
                items:
                    type: object
                    properties:
                        userId:
                            type: integer
                            example: 1
                        id:
                            type: integer
                            example: 1
                        title:
                            type: string
                            example: "Título do post"
                        body:
                            type: string
                            example: "Conteúdo do post"
        401:
            description: Não Autorizado
    """
    acess_level = get_access_level_by_id(user_id)
    if acess_level < 3:
        return jsonify({'error': 'Não Autorizado'}), 401
    response = requests.get(f'{_URL_BASE_}/posts')
    posts = response.json()
    return jsonify(posts), 200

@app.route('/external/posts/<int:post_id>/<int:user_id>', methods=['GET'])
def get_post(post_id, user_id):
    """
    Obter um post específico por ID, desde que o user tenha acesso.
    Necessário acesso de nível 1 ou maior.
    ---
    parameters:
        - name: post_id
          in: path
          type: integer
          required: true
          description: ID do post
        - name: user_id
          in: path
          type: integer
          required: true
          description: ID do usuario
    responses:
        200:
            description: Post específico
            schema:
                type: object
                properties:
                    userId:
                        type: integer
                        example: 1
                    id:
                        type: integer
                        example: 1
                    title:
                        type: string
                        example: "Título do post"
                    body:
                        type: string
                        example: "Conteúdo do post"
        401:
            description: Não Autorizado
    """
    acess_level = get_access_level_by_id(user_id)
    if acess_level < 1:
        return jsonify({'error': 'Não Autorizado'}), 401
    response = requests.get(f'{_URL_BASE_}/posts/{post_id}')
    post = response.json()
    return jsonify(post), 200

@app.route('/external/cep/<string:cep>/<int:user_id>', methods=['GET'])
def get_cep(cep, user_id):
    """
    Obter informações sobre um CEP, desde que o user tenha acesso.
    Necessário acesso de nível 2 ou maior.
    ---
    parameters:
        - name: cep
          in: path
          type: string
          required: true
          description: CEP a ser consultado
        - name: user_id
          in: path
          type: integer
          required: true
          description: ID do usuario
    responses:
        200:
            description: Informações sobre o CEP
            schema:
                type: object
                properties:
                    cep:
                        type: string
                        example: "01001-000"
                    logradouro:
                        type: string
                        example: "Praça da Sé"
                    complemento:
                        type: string
                        example: "lado ímpar"
                    bairro:
                        type: string
                        example: "Sé"
                    localidade:
                        type: string
                        example: "São Paulo"
                    uf:
                        type: string
                        example: "SP"
                    ibge:
                        type: string
                        example: "3550308"
                    gia:
                        type: string
                        example: "1004"
                    ddd:
                        type: string
                        example: "11"
                    siafi:
                        type: string
                        example: "7107"
        400:
            description: CEP inválido
        401:
            description: Não Autorizado
        404:
            description: CEP não encontrado
    """
    acess_level = get_access_level_by_id(user_id)
    if acess_level < 2:
        return jsonify({'error': 'Não Autorizado'}), 401
    response = requests.get(f'{_URL_BASE_}/cep/{cep}')
    if response.status_code == 200:
        data = response.json()
        if 'erro' in data:
            return jsonify({'error': 'CEP não encontrado'}), 404
        return jsonify(data), 200
    return jsonify({'error': 'CEP inválido'}), 400

if __name__ == '__main__':
    port = 5002
    app.run(debug=True, host='0.0.0.0', port=port)
