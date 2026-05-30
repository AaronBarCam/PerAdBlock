from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()

# Cargamos el modelo entrenado
model = joblib.load('modelo_peradblock.pkl')
vectorizer = joblib.load('vectorizador_peradblock.pkl')

class URLItem(BaseModel):
    url: str

@app.post("/predict")
async def predict(item: URLItem):
    vectorized_url = vectorizer.transform([item.url])
    probabilidades = model.predict_proba(vectorized_url)[0] # [Prob_Limpio, Prob_Ad]
    prob_ad = probabilidades[1]
    
    # Solo bloqueamos si estamos MUY seguros (ej: > 80%)
    is_ad = prob_ad > 0.80 
    
    return {
        "url": item.url,
        "is_ad": bool(is_ad),
        "confidence": float(prob_ad)
    }