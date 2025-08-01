from models import Usuario, db
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=db)

def pegar_sessao():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
