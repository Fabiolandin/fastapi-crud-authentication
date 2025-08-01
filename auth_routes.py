from fastapi import APIRouter, Depends
from models import Usuario
from dependencies import pegar_sessao

#Criando roteador de rota com prefixo de /auth
auth_router = APIRouter(prefix="/auth", tags=["auth"])

#Criando rotas

@auth_router.get("/")
async def autenticar():
    """ Rota padrão de auntenticação do sistema. """
    return {"mensagem": "Você acessou a rota de autenticação"}

@auth_router.post("/criar_conta")
async def criar_conta(email: str, senha: str, nome: str, session = Depends(pegar_sessao)):
    """ Rota para criar uma nova conta de usuário. """
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        return {"mensagem": "Já existe usuário com este email"}
    else:
        novo_usuario = Usuario(nome, email, senha)
        session.add(novo_usuario)
        session.commit()
    return {"mensagem": "Conta criada com sucesso"}