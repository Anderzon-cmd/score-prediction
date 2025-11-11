from pydantic import BaseModel,Field

class PredictQuoteRequest(BaseModel):
    edad_mascota:int =Field(...,ge=0,title="Edad de mascota")
    edad_cliente:int =Field(...,ge=1,title="Edad de cliente")
    hora_cita:int =Field(...,ge=0,title="Hora de la cita")
    dia_semana:int =Field(...,ge=0,le=6,title="Dia de la semana de la cita")
