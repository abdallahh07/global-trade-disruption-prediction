from fastapi import FastAPI
from pydantic import BaseModel
from predict import make_prediction

app = FastAPI()

class PredictionInput(BaseModel):
    oil_brent: float
    natural_gas: float
    wheat: float
    corn: float
    gold: float
    aluminum: float
    iron_ore: float
    is_covid_period: int
    is_russia_ukraine_period: int
    is_red_sea_period: int
    is_hormuz_period: int
