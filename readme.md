# Projeto de APIs com Flask e Swagger

Este projeto consiste em duas APIs simples desenvolvidas com Flask e Swagger para CRUD de usuários. Cada API está contida em seu próprio diretório e pode ser executada utilizando Docker e Docker Compose.

## Estrutura do Projeto

/  
├── backendExternal/  
│ ├── app.py  
│ ├── Dockerfile  
│ └── requirements.txt  
├── backendUser/  
│ ├── app.py  
│ ├── Dockerfile  
│ └── requirements.txt  
└── docker-compose.yml  


## Pré-requisitos

- Docker: [Instale o Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Instale o Docker Compose](https://docs.docker.com/compose/install/)

## Configuração

### Passo 1: Clone o Repositório

Clone este repositório em sua máquina local:

```sh
git clone https://github.com/senhorbento/MVP-Software-Architecture
cd MVP-Software-Architecture
git clone https://github.com/senhorbento/backendExternal
```

## Executar o Projeto
Navegue até o diretório raiz do projeto:

```sh
cd path/to/mvp-software-architecture
```
Execute o Docker Compose:

```sh
docker-compose up --build
```
Para acessar o Swagger, acesse um dos links através do seu navegador

Backend User: http://127.0.0.1:5001/apidocs  
Backend External: http://127.0.0.1:5002/apidocs