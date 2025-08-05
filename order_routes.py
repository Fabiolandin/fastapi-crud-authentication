from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema, ProdutoSchema, ResponsePedidoSchema
from models import Pedido, Usuario, ItemPedido, Produto
from typing import List

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
    
@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido:int, item_pedido_schema: ItemPedidoSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Rota para adicionar item ao pedido."""
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    produto = session.query(Produto).filter(Produto.id == item_pedido_schema.produto).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin or usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para adicionar itens a este pedido")
    if not produto:
        raise HTTPException(status_code=400, detail="Produto não encontrado")
    
    item_pedido = ItemPedido(quantidade=item_pedido_schema.quantidade, preco_unitario=item_pedido_schema.preco_unitario, pedido=id_pedido, produto=item_pedido_schema.produto)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {"mensagem": "Item adicionado ao pedido com sucesso", "item": produto.nome}


@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido:int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Rota para remover item do pedido."""
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin or usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para adicionar itens a este pedido")
    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {"mensagem": "Item removido com sucesso","quantidade_itens_pedido": len(pedido.itens), "pedido": pedido}

#Finalizar pedido por id
@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Rota para cancelamento de pedidos."""
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin or usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce não tem autorização para cancelar este pedido")
    pedido.status = "FINALIZADO"
    session.commit()
    return {"mensagem": f"Pedido ID: {pedido.id} finalizado com sucesso", "pedido": pedido}

#Visualizar pedido por id de pedido
@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Rota para visualizar detalhes de um pedido específico."""
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para visualizar este pedido")
    return {"quantidade_itens_pedido": len(pedido.itens), "pedido": pedido}

@order_router.get("/listar/pedidos-usuario}", response_model=List[ResponsePedidoSchema])
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Rota para listar pedidos da conta em que está logada. """
    pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
    return pedidos