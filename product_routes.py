from fastapi import APIRouter


#Criando roteador de rota com prefixo de /product
product_router = APIRouter(prefix="/product", tags=["product"])

#Criando rotas

@product_router.get("/")
async def produtos():
    """ Rota padrão de produtos do sistema. Todas as rotas de produtos precisam de autenticação. """
    return {"mensagem": "Você acessou a rota de produtos"}