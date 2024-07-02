from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
swagger = Swagger(app)

# Modelo do Usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    have_access = db.Column(db.Boolean, default=True)

# Criar o banco de dados
db.create_all()

# Endpoint para criar um novo usuário
@app.route('/users', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'Usuário criado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'user': {'type': 'string'},
                    'password': {'type': 'string'},
                    'have_access': {'type': 'boolean'}
                }
            }
        }
    }
})
def create_user():
    data = request.get_json()
    new_user = User(user=data['user'], password=data['password'], have_access=data['have_access'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.id), 201

# Endpoint para obter todos os usuários
@app.route('/users', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Lista de todos os usuários',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'user': {'type': 'string'},
                        'password': {'type': 'string'},
                        'have_access': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'user': user.user, 'password': user.password, 'have_access': user.have_access} for user in users]), 200

# Endpoint para obter um usuário específico por ID
@app.route('/users/<int:user_id>', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do usuário'
        }
    ],
    'responses': {
        200: {
            'description': 'Detalhes do usuário',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'user': {'type': 'string'},
                    'password': {'type': 'string'},
                    'have_access': {'type': 'boolean'}
                }
            }
        },
        404: {
            'description': 'Usuário não encontrado'
        }
    }
})
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'id': user.id, 'user': user.user, 'password': user.password, 'have_access': user.have_access}), 200

# Endpoint para atualizar um usuário específico por ID
@app.route('/users/<int:user_id>', methods=['PUT'])
@swag_from({
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do usuário'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'user': {'type': 'string'},
                    'password': {'type': 'string'},
                    'have_access': {'type': 'boolean'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Usuário atualizado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'user': {'type': 'string'},
                    'password': {'type': 'string'},
                    'have_access': {'type': 'boolean'}
                }
            }
        },
        404: {
            'description': 'Usuário não encontrado'
        }
    }
})
def update_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    user.user = data['user']
    user.password = data['password']
    user.have_access = data['have_access']
    db.session.commit()
    return jsonify({'id': user.id, 'user': user.user, 'password': user.password, 'have_access': user.have_access}), 200

# Endpoint para deletar um usuário específico por ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
@swag_from({
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do usuário'
        }
    ],
    'responses': {
        200: {
            'description': 'Usuário deletado com sucesso'
        },
        404: {
            'description': 'Usuário não encontrado'
        }
    }
})
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 200

if __name__ == '__main__':
    app.run(debug=True)
