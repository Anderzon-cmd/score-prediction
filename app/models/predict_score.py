from pydantic import BaseModel,Field

class PredictScoreRequest(BaseModel):
    identify_verified:int =Field(...,ge=0,le=1,title="Identidad verificada")
    loan_count:int =Field(...,ge=1,title="Cantidad de prestamos")
    adress_verified:int =Field(...,ge=0,le=1,title="Direccion verificada")
