from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS solo para DEV
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En PROD poner dominio real
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend funcionando"}

@app.get("/api/health")
def health():
    return {"status": "ok"}