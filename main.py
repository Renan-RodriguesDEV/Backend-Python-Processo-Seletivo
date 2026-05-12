from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.locations import router as locations_router
from routes.reservations import router as reservations_router
from routes.rooms import router as rooms_router

app = FastAPI(title="Processo Seletivo API - Backend Python", version="1.0.0")

app.include_router(locations_router)
app.include_router(rooms_router)
app.include_router(reservations_router)

# Configuração de CORS para permitir requisições de qualquer origem, no caso o frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Processo Seletivo API - Backend Python"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
