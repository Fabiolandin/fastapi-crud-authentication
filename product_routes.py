from fastapi import APIRouter, Depends, HTTPException
from models import Produto, Usuario, ItemPedido
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

@product_router.post("/product/delete/{id_produto}")
async def deletar_produto(id_produto: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Rota para deletar produtos. """
    produto = session.query(Produto).filter(Produto.id == id_produto).first()
    if not produto:
        raise HTTPException(status_code=400, detail="Produto não encontrado")
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para deletar produtos")
    item_vinculado = session.query(ItemPedido).filter(ItemPedido.produto == id_produto).first()
    if item_vinculado:
        raise HTTPException(status_code=400, detail="Produto vinculado a um pedido, não pode ser deletado")
    session.delete(produto)
    session.commit()
    return {"mensagem": f"Produto {produto.nome} deletado com sucesso"}
