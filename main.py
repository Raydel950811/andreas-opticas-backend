from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def health_check():
    return {
        "status": "online",
        "brand": "Andreas Ópticas",
        "mensaje": "¡Servidor en Render funcionando perfectamente!"
    }
