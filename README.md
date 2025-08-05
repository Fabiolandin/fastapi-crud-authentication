# 🔐 FastAPI - CRUD com Autenticação

Este é um projeto simples de uma API feita com **FastAPI**. O foco principal foi praticar um CRUD com autenticação JWT. O projeto simula um sistema de cadastro e login de usuários, com rotas protegidas por token.

Desenvolvi esse projeto como parte dos meus estudos em backend com Python. Ele representa um passo importante no meu aprendizado com FastAPI, SQLAlchemy e autenticação de usuários.

---

## 🚀 Tecnologias usadas

- Python
- FastAPI
- SQLAlchemy
- JWT (python-jose)
- Passlib (para hash de senhas)
- SQLite (como banco de dados)
- Uvicorn (servidor)

---

## 📁 Estrutura do Projeto

📦 app/
**Descrição dos arquivos**:
- `main.py`: Configuração principal do FastAPI e rotas da API
- `models.py`: Define as tabelas do banco de dados usando SQLAlchemy
- `schemas.py`: Modelos Pydantic para validação de dados
- `crud.py`: Contém as operações básicas do banco de dados
- `auth.py`: Implementa autenticação JWT (login, registro, etc.)
- `database.py`: Configura a conexão com o PostgreSQL e sessão do SQLAlchemy

---

🔐 Funcionalidades
Cadastro de usuários

Login com geração de token JWT

Rotas protegidas com token

Atualização e remoção de usuário

📌 Exemplo de uso
**Login**
POST /token  
Content-Type: application/x-www-form-urlencoded

username=fabio&password=123456

**Acesso a rota protegida**
GET /users/me  
Authorization: Bearer SEU_TOKEN_AQUI

---
✍️ Sobre mim
Sou o Fábio Landin, apaixonado por tecnologia desde criança e focado em transição de carreira para a área de desenvolvimento. Estou estudando Python com foco em backend e APIs com FastAPI.

Se quiser trocar uma ideia, me chama lá no LinkedIn.
---

### ✅ O que você precisa fazer:

- Substitua `https://www.linkedin.com/in/fabio-landin-a76867262/` pelo seu link verdadeiro do LinkedIn.

Desenvolvido com ❤️ por Fabio Landin
