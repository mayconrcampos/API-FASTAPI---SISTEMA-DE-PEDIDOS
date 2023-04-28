from fastapi import FastAPI
from core.configs import settings
from api.v1.api import api_router
from functools import lru_cache


app = FastAPI(title="API - SISTEMA DE CADASTRO DE CLIENTES E PEDIDOS")
app.include_router(api_router, prefix=settings.API_V1_STR)

@lru_cache()
def get_settings():
    return settings

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)