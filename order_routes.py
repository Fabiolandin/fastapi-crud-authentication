from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema
from models import Pedido, Usuario

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def pedidos():
    """ Rota padrão de pedidos do sistema. Todas as rotas de pedidos precisam de autenticação. """
    return {"mensagem": "Você acessou a rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Rota para criar pedidos."""
    usuario_existente = session.query(Usuario).filter(Usuario.id == pedido_schema.usuario).first()
    if not usuario_existente:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso para o usuário ID: {novo_pedido.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Rota para cancelamento de pedidos."""
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin or usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce não tem autorização para cancelar este pedido")
    pedido.status = "CANCELADO"
    session.commit()
    return {"mensagem": f"Pedido ID: {pedido.id} cancelado com sucesso", "pedido": pedido}


@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Rota para listar pedidos. """
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para listar pedidos")
    else:
        pedidos = session.query(Pedido).all()
        return {"pedidos": pedidos}