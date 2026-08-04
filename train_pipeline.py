import joblib
from pathlib import Path
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from processing.data_manager import load_dataset, save_pipeline
from config.config import config
from processing.features import merge_commodities, merge_gdelt, merge_comtrade, build_master, get_x_y
from pipeline import pipe
import os

def run_training():
  
    dataframes = {
        "oil_wti": load_dataset(config.oil_wti),
        "oil_brent": load_dataset(config.oil_brent),
        "natural_gas": load_dataset(config.natural_gas),
        "wheat": load_dataset(config.wheat),
        "corn": load_dataset(config.corn),
        "gold": load_dataset(config.gold),
        "aluminum": load_dataset(config.aluminum),
        "iron_ore": load_dataset(config.iron_ore),
        "gdelt_strait_of_hormuz": load_dataset(config.gdelt_strait_of_hormuz),
        "gdelt_red_sea_shipping": load_dataset(config.gdelt_red_sea_shipping),
        "gdelt_russia_ukraine_conflict": load_dataset(config.gdelt_russia_ukraine_conflict),
        "gdelt_covid_supply_chain": load_dataset(config.gdelt_covid_supply_chain),
        "comtrade_egypt": load_dataset(config.comtrade_egypt),
        "comtrade_iran": load_dataset(config.comtrade_iran),
        "comtrade_china": load_dataset(config.comtrade_china),
        "comtrade_usa": load_dataset(config.comtrade_usa),
    }

    commodities = merge_commodities(dataframes)
    gdelt = merge_gdelt(dataframes)
    comtrade = merge_comtrade(dataframes)

    master = build_master(commodities, gdelt, comtrade)
    master = master.sort_values("date")

    x, y = get_x_y(master)

    split = int(len(master) * config.split_rate)
    x_train = x.iloc[:split]
    x_test = x.iloc[split:]
    y_train = y.iloc[:split]
    y_test = y.iloc[split:]

    pipe.fit(x_train, y_train)
    y_pred = pipe.predict(x_test)

    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    print(f"R2: {r2}, MAE: {mae}, MSE: {mse}")

    save_pipeline(pipe)
    joblib.dump(list(x_train.columns), "trained_model/feature_names.pkl")


if __name__ == "__main__":
    run_training()