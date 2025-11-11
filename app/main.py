import keras
import tensorflow as tf
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import os
import numpy as np
from app.log.config import logger
from app.models.predict_score import PredictScoreRequest
from fastapi.middleware.cors import CORSMiddleware
from app.models.predict_quote import PredictQuoteRequest
import pandas as pd
import joblib

def get_model_predict(model_name:str):
    path=os.path.join("app","ml-models",model_name)
    return keras.models.load_model(path)


@asynccontextmanager
async def lifespan(app:FastAPI):
    model=get_model_predict("score_loan.keras")
    app.state.model_predict_score=model
    print("Model predict-score load is successfuly")

    model_quote=get_model_predict("predict-citas.keras")
    app.state.model_predict_quote=model_quote
    print("Model predict-quote load is successfuly")

    app.state.param_predict_quote=joblib.load(os.path.join("app","ml-models","normalization_predict_quote.pkl"))
    print("Params to normalized load is successfuly")

    yield
    print("Application shutdown")

app=FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/predict-score",)
def predict_score(request:PredictScoreRequest):
    data_to_predict={
        "identify_verified":np.array([request.identify_verified]),
        "loan_count":np.array([request.loan_count]),
        "adress_verified":np.array([request.adress_verified])
        }
    try:
        score=app.state.model_predict_score.predict(data_to_predict)[0][0]
        return {
            "score":round(float(score),4)
        }
    except Exception as ex:
        logger.error(ex)
        raise HTTPException(status_code=400,detail="Error predict score")
    
@app.post("/predict-quote")
def predict_quote(request: PredictQuoteRequest):
    # Crear DataFrame
    new_predict = pd.DataFrame([{
        'edad_mascota': request.edad_mascota,
        'edad_cliente': request.edad_cliente,
        'hora_cita': request.hora_cita,
        'dia_semana': request.dia_semana,
    }])

    # Normalizar
    params = app.state.param_predict_quote
    data_normalize = (new_predict - params["mean"]) / params["std"]

    input_dict = {col: data_normalize[[col]].to_numpy() for col in ['edad_cliente','edad_mascota','hora_cita','dia_semana']}

    try:
        quote = app.state.model_predict_quote.predict(input_dict)[0][0]
        return {"asistencia_cita": round(float(quote), 3)}

    except Exception as ex:
        logger.error(ex)
        print(ex)
        raise HTTPException(status_code=400, detail="Error predict quote cancelled")




    