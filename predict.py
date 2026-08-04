import pandas as pd
from processing.data_manager import load_pipeline

pipeline = load_pipeline()

def make_prediction(input_data: dict) -> float:
    input_df = pd.DataFrame([input_data])
    prediction = pipeline.predict(input_df)
    return prediction[0]