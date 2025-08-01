from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

#instanciando objeto/criando servidor
app = FastAPI()

#instanciando objeto de criptografia
bcryp_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Importando os roteadores de rota
from auth_routes import auth_router
from product_routes import product_router

#incluindo no arquivo os roteadores de rota de auth e product
app.include_router(auth_router)
app.include_router(product_router)