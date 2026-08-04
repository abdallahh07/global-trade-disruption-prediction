from fastapi import APIRouter
from app.schemas import PredictionInput
from predict import make_prediction

router = APIRouter()

@router.post("/predict")
def predict(input_data: PredictionInput):
    result = make_prediction(input_data.dict())
    return {"prediction": result}