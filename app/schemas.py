from pydantic import BaseModel

class PredictResponse(BaseModel):
    label: str         # La etiqueta que predijo el modelo
    confidence: float  # La confianza (entre 0 y 1)

class FeedbackRequest(BaseModel):
    predicted: str     # Etiqueta que el modelo entregó
    correct: str       # Etiqueta correcta según el usuario