from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool] = False

    class Config:
        from_attributes = True

class ProdutoSchema(BaseModel):
    nome: str
    descricao: str
    preco: float

    class Config:
        from_attributes = True


class PedidoSchema(BaseModel):
    usuario: int

    class Config:
        from_attributes = True