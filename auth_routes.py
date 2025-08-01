from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcryp_context
from schemas import UsuarioSchema
from sqlalchemy.orm import Session

#Criando roteador de rota com prefixo de /auth
auth_router = APIRouter(prefix="/auth", tags=["auth"])

#Criando rotas

@auth_router.get("/")
async def autenticar():
    """ Rota padrão de auntenticação do sistema. """
    return {"mensagem": "Você acessou a rota de autenticação"}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    """ Rota para criar uma nova conta de usuário. """
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        return HTTPException(status_code=400, detail="Usuário já existe com este email")
    else:
        senha_criptografada = bcryp_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
    return {"mensagem": f"Conta criada com sucesso {usuario_schema.email}"}