from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from content_engine import generate_reel_content

app = FastAPI(title="Andreas Ópticas - Content Engine")

class ContentRequest(BaseModel):
    topic_angle: str

@app.get("/")
def health_check():
    return {
        "status": "online",
        "brand": "Andreas Ópticas",
        "mensaje": "¡El motor de IA está listo para recibir peticiones!"
    }

@app.post("/api/v1/content/generate")
async def generate_content(payload: ContentRequest):
    try:
        script_data = await generate_reel_content(payload.topic_angle)
        return {
            "status": "success",
            "brand": "Andreas Ópticas",
            "generated_script": script_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando contenido con IA: {str(e)}")
