import keras
import tensorflow as tf
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import os
import numpy as np
from app.log.config import logger
from app.models.predict_score import PredictScoreRequest
from fastapi.middleware.cors import CORSMiddleware

def get_model_predict_score():
    path=os.path.join("app","ml-models","score_loan.keras")
    return keras.models.load_model(path)
    

@asynccontextmanager
async def lifespan(app:FastAPI):
    model=get_model_predict_score()
    global model_t
    model_t=model
    app.state.model_predict_score=model
    print("Model load is successfuly")
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


    