from pydantic import BaseModel,Field

class PredictScoreRequest(BaseModel):
    identify_verified:int =Field(...,ge=0,le=1,title="Identidad verificada")
    loan_count:int =Field(...,ge=1,title="Cantidad de prestamos")
    adress_verified:int =Field(...,ge=0,le=1,title="Direccion verificada")
    late_payment_count:int=Field(...,ge=0,title="Cantidad de pagos tardios")
    avg_days_late:float=Field(...,ge=0,title="Promedio de dias en morra")
    total_penalty:float=Field(...,ge=0,title="Monto total de penalidades")
    fraud_report_count:int=Field(...,ge=0,le=2,title="Cantidad de reporte por fraude")

