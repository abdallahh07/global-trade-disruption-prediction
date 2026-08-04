import pandas as pd
from config.config import config

def merge_commodities(dataframes: dict) -> pd.DataFrame:
    commodities = dataframes["oil_wti"].rename(columns={"value": "oil_wti"})
    commodities = pd.merge(commodities, dataframes["oil_brent"].rename(columns={"value": "oil_brent"}), on="date", how="left")
    commodities = pd.merge(commodities, dataframes["natural_gas"].rename(columns={"value": "natural_gas"}), on="date", how="left")
    commodities = pd.merge(commodities, dataframes["wheat"].rename(columns={"value": "wheat"}), on="date", how="left")
    commodities = pd.merge(commodities, dataframes["corn"].rename(columns={"value": "corn"}), on="date", how="left")
    commodities = pd.merge(commodities, dataframes["gold"].rename(columns={"value": "gold"}), on="date", how="left")
    commodities = pd.merge(commodities, dataframes["aluminum"].rename(columns={"value": "aluminum"}), on="date", how="left")
    commodities = pd.merge(commodities, dataframes["iron_ore"].rename(columns={"value": "iron_ore"}), on="date", how="left")
    commodities["date"] = pd.to_datetime(commodities["date"])
    return commodities

def merge_gdelt(dataframes: dict) -> pd.DataFrame:
    gdelt = dataframes["gdelt_strait_of_hormuz"].rename(columns={"value": "hormuz_risk"})
    gdelt = pd.merge(gdelt, dataframes["gdelt_red_sea_shipping"].rename(columns={"value": "red_sea_risk"}), on="date", how="left")
    gdelt = pd.merge(gdelt, dataframes["gdelt_russia_ukraine_conflict"].rename(columns={"value": "russia_ukraine_risk"}), on="date", how="left")
    gdelt = pd.merge(gdelt, dataframes["gdelt_covid_supply_chain"].rename(columns={"value": "covid_risk"}), on="date", how="left")
    gdelt["date"] = pd.to_datetime(gdelt["date"]).dt.tz_localize(None)
    return gdelt

def merge_comtrade(dataframes: dict) -> pd.DataFrame:
    comtrade = dataframes["comtrade_egypt"][["period", "primaryValue"]].rename(columns={"primaryValue": "egypt_trade_value"})
    comtrade = pd.merge(comtrade, dataframes["comtrade_iran"][["period", "primaryValue"]].rename(columns={"primaryValue": "iran_trade_value"}))
    comtrade = pd.merge(comtrade, dataframes["comtrade_china"][["period", "primaryValue"]].rename(columns={"primaryValue": "china_trade_value"}))
    comtrade = pd.merge(comtrade, dataframes["comtrade_usa"][["period", "primaryValue"]].rename(columns={"primaryValue": "usa_trade_value"}))
    comtrade["period"] = pd.to_datetime(comtrade["period"], format="%Y")
    comtrade = comtrade.rename(columns={"period": "date"})
    return comtrade

def build_master(commodities: pd.DataFrame, gdelt: pd.DataFrame, comtrade: pd.DataFrame) -> pd.DataFrame:
    master = pd.merge(commodities, gdelt, on="date", how="left")
    master = pd.merge(master, comtrade, on="date", how="left")

    for col in ["oil_wti", "oil_brent", "natural_gas", "wheat", "corn", "gold", "aluminum", "iron_ore"]:
        master[col] = pd.to_numeric(master[col], errors="coerce")

    for col in config.ffill_columns:
        master[col] = master[col].ffill()

    master = master.dropna(subset=config.ffill_columns)   # <-- add it here

    master["is_covid_period"] = ((master["date"] >= "2020-02-01") & (master["date"] <= "2020-12-31")).astype(int)
    master["is_russia_ukraine_period"] = ((master["date"] >= "2022-02-24") & (master["date"] <= "2022-12-31")).astype(int)
    master["is_red_sea_period"] = ((master["date"] >= "2023-11-01") & (master["date"] <= "2024-12-31")).astype(int)
    master["is_hormuz_period"] = (master["date"] >= "2026-02-28").astype(int)

    return master

def get_x_y(master: pd.DataFrame):
    x = master.drop(columns=config.features_to_drop)
    y = master[config.target]
    return x, y