from fastapi import FastAPI
from auth_routes import auth_router
from product_routes import product_router

#instanciando objeto/criando servidor
app = FastAPI()

#incluindo no arquivo os roteadores de rota de auth e product
app.include_router(auth_router)
app.include_router(product_router)