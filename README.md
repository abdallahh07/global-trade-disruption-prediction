# global-trade-disruption-prediction
Predicts commodity price movements (WTI crude oil) from global supply chain disruption signals — geopolitical events (GDELT), trade flows (UN Comtrade), and logistics performance (World Bank), built on real API data rather than synthetic sources.

## What This Predicts

**Target:** percentage change in WTI crude oil price over a forward window
(e.g. next 30 days), given current disruption signals — not the raw price
level, to avoid the model just learning long-term inflation trends.

## Data Sources (real APIs, no synthetic data)

| Source | What it provides | Role |
|---|---|---|
| FRED API | WTI oil price history | Target variable + lagged/momentum features |
| GDELT | Geopolitical event intensity, conflict scores | Primary disruption signal |
| UN Comtrade API | Bilateral trade volume between countries | Supply-side secondary signal |
| World Bank API | Logistics Performance Index, GDP, trade % of GDP | Slower-moving country-level context |

## Planned Tech Stack

- Python, pandas, NumPy
- scikit-learn, XGBoost, LightGBM, CatBoost (model comparison, same as prior projects)
- FastAPI + Uvicorn for serving predictions
- Docker + Railway for deployment
- joblib for pipeline serialization

## Roadmap

- [ ] `scripts/fred_collector.py` — pull WTI oil price history
- [ ] `scripts/gdelt_collector.py` — pull geopolitical event scores
- [ ] `scripts/comtrade_collector.py` — pull bilateral trade volume
- [ ] `scripts/worldbank_collector.py` — pull Logistics Performance Index, GDP
- [ ] Merge all sources into one dataset, aligned by date
- [ ] Construct target column (% change in oil price, forward window)
- [ ] EDA — distributions, correlations, event-driven anomalies (COVID, Russia-Ukraine, Red Sea, Hormuz)
- [ ] Feature engineering (lagged values, rolling windows, event intensity aggregation)
- [ ] Model comparison (RandomForest, GradientBoosting, XGBoost, CatBoost, LightGBM)
- [ ] Standard production package structure (config, processing, pipeline, train_pipeline, predict, app/)
- [ ] Dockerfile + Railway deployment

## Project Structure (planned)
global-trade-disruption-prediction/
├── data/
├── notebooks/
│ └── research.ipynb
├── scripts/
│ ├── fred_collector.py
│ ├── gdelt_collector.py
│ ├── comtrade_collector.py
│ └── worldbank_collector.py
├── config/
├── processing/
├── app/
├── pipeline.py
├── train_pipeline.py
├── predict.py
├── Dockerfile
└── requirements.txt

## Status

🚧 In progress — data collection phase.
