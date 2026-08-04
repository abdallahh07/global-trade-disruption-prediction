from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression

model = LinearRegression()

pipe = Pipeline([
        ("scaler",StandardScaler()),
        ("Model",model)])