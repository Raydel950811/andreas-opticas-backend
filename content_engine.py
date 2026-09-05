import json
from typing import List, Literal
from pydantic import BaseModel, Field
from openai import AsyncOpenAI
import os

client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class ReelScriptSchema(BaseModel):
    selected_hook: str = Field(..., description="El gancho seleccionado de la matriz de entrada.")
    hook_category: Literal["Salud Visual", "Estética", "Curiosidad"] = Field(..., description="Categoría del gancho utilizado.")
    voiceover_script: str = Field(..., description="Guión completo para la voz en off en formato natural de locución (máx 60 palabras).")
    visual_cues: List[str] = Field(..., description="Sugerencias de tomas o recursos visuales para el renderizado.")
    caption: str = Field(..., description="Copy final para la publicación en Instagram con saltos de línea y emojis.")
    cta_trigger_word: str = Field(..., description="Palabra clave exacta del CTA (ej. ESTILO, EXAMEN, PANTALLA).")
    selected_cta: str = Field(..., description="Llamado a la acción seleccionado de la matriz.")
    hashtags: List[str] = Field(..., description="5 a 8 hashtags optimizados para SEO local e Instagram.")

SYSTEM_PROMPT = """
Eres el Director de Contenido y Copywriter Senior de la marca "Andreas Ópticas".
Tu objetivo es escribir guiones de Reels de 30 segundos optimizados para ALTA CONVERSIÓN y retención de audiencia.

CONTEXTO DE MARCA:
- Nombre: Andreas Ópticas.
- Nicho: Salud visual, monturas de diseño, gafas de sol, lentes de contacto y protección de pantallas.
- Público Objetivo: Personas preocupadas por su estética pero con necesidades de corrección visual, usuarios intensivos de pantallas con fatiga ocular.
- Tono: Profesional, moderno, empático y dinámico.

REGLAS DE GENERACIÓN OBLIGATORIAS:
1. MATRIZ DE GANCHOS (Debes seleccionar estrictamente UNO para los primeros 3 segundos):
   [Salud Visual]
   - "Si pasas más de 4 horas al día frente a pantallas, tus ojos están haciendo esto sin que te des cuenta..."
   - "Detente: si sientes la vista cansada a las 5:00 PM, el problema no es el estrés, es tu tipo de lente."
   [Estética]
   - "El error del 90% de las personas al elegir gafas: usar este marco si tienes el rostro redondo."
   - "3 monturas de Andreas Ópticas que literalmente te afinan las facciones."
   [Curiosidad]
   - "3 cosas que arruinan tus gafas en menos de 6 meses (y la número 2 la haces todos los días)."

2. MATRIZ DE CTAs (Cierre obligatorio orientado a conversión):
   [Captación] - Palabra clave: ESTILO
   [Agendamiento] - Palabra clave: EXAMEN
   [Venta] - Palabra clave: PANTALLA
"""

async def generate_reel_content(topic_angle: str) -> ReelScriptSchema:
    response = await client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Crea un guión enfocado en el siguiente ángulo/tema: '{topic_angle}'."}
        ],
        response_format=ReelScriptSchema,
        temperature=0.7,
    )
    return response.choices[0].message.parsed
