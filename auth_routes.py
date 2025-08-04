from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from main import bcryp_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

#Criando roteador de rota com prefixo de /auth
auth_router = APIRouter(prefix="/auth", tags=["auth"])

#Função para criar token JWT
def criar_token(id_usuario, duracao_token=ACCESS_TOKEN_EXPIRE_MINUTES):
    data_expiracao = datetime.now(timezone.utc) + timedelta(minutes=duracao_token)
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado

#Autenticação de usuário - vai pesquisar no banco de dados o email e senha do usuário e ver se bate
def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcryp_context.verify(senha, usuario.senha):
        return False
    return usuario

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


@auth_router.post("/login")
async def login(login_schema:LoginSchema, session: Session = Depends(pegar_sessao)):
    """ Rota para login de users. """
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=7*24*60)  # 7 dias
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    
@auth_router.post("/login-form")
async def login(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    """ Rota para login de users. """
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        return {"access_token": access_token, "token_type": "bearer"}
    
@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    acess_token = criar_token(usuario.id)
    return {"acess_token": acess_token, "token_type": "bearer"}