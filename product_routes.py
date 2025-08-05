from fastapi import APIRouter, Depends, HTTPException
from models import Produto, Usuario
from dependencies import pegar_sessao, verificar_token
from schemas import ProdutoSchema
from sqlalchemy.orm import Session

#Criando roteador de rota com prefixo de /product
product_router = APIRouter(prefix="/product", tags=["produtos"])

#Criando rotas

@product_router.get("/")
async def produtos():
    """ Rota padrão de produtos do sistema. Todas as rotas de produtos precisam de autenticação. """
    return {"mensagem": "Você acessou a rota de produtos"}

@product_router.post("/criar_produto")
async def criar_produto(produto_schema: ProdutoSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Rota para criação de produtos. """
    # Só admin pode criar produtos
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para criar produtos")
    novo_produto = Produto(produto_schema.nome, produto_schema.descricao, produto_schema.preco)
    session.add(novo_produto)
    session.commit()
    return {"mensagem": f"Produto {produto_schema.nome} criado com sucesso"}
