from flask import Flask, jsonify
import requests
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Endpoint para obter posts
@app.route('/posts', methods=['GET'])
def get_posts():
    """
    Obter todos os posts
    ---
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
    """
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    posts = response.json()
    return jsonify(posts), 200

# Endpoint para obter um post específico por ID
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """
    Obter um post específico por ID
    ---
    parameters:
        - name: post_id
          in: path
          type: integer
          required: true
          description: ID do post
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
    """
    response = requests.get(f'https://jsonplaceholder.typicode.com/posts/{post_id}')
    post = response.json()
    return jsonify(post), 200

if __name__ == '__main__':
    app.run(debug=True)
