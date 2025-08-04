from models import Usuario, db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema

SessionLocal = sessionmaker(bind=db)

def pegar_sessao():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usurio = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso negado, verifique a validade do token!")
    usuario = session.query(Usuario).filter(Usuario.id==id_usurio).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso invalido!")
    return usuario
