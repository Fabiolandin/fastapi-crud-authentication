from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import PedidoSchema
from models import Pedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_router.get("/")
async def pedidos():
    """ Rota padrão de pedidos do sistema. Todas as rotas de pedidos precisam de autenticação. """
    return {"mensagem": "Você acessou a rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    """ Rota para criar pedidos."""
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso para o usuário ID: {novo_pedido.id}"}