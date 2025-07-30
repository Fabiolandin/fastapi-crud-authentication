from fastapi import APIRouter

#Criando roteador de rota com prefixo de /auth
auth_router = APIRouter(prefix="/auth", tags=["auth"])

#Criando rotas

@auth_router.get("/")
async def autenticar():
    """ Rota padrão de auntenticação do sistema. """
    return {"mensagem": "Você acessou a rota de autenticação"}