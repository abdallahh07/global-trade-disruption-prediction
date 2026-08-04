from pathlib import Path
from typing import List 
from pydantic import BaseModel
import yaml

PACKAGE_ROOT = Path(__file__).parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"

class AppConfig(BaseModel):
  pipeline_name: str
  pipeline_save_file: str
  data_folder: str
  aluminum: str
  corn: str
  wheat: str
  gold: str
  iron_ore: str
  natural_gas: str
  oil_brent: str
  oil_wti: str
  comtrade_china: str
  comtrade_egypt: str
  comtrade_iran: str
  comtrade_usa: str
  gdelt_covid_supply_chain: str
  gdelt_red_sea_shipping: str
  gdelt_russia_ukraine_conflict: str
  gdelt_strait_of_hormuz: str
  split_rate : float
  target: str
  features : List[str]
  ffill_columns: List[str]
  features_to_drop: List[str]
  
def fetch_config_from_yaml()-> AppConfig:
  with open (CONFIG_FILE_PATH ,"r") as f :
    parsed = yaml.safe_load(f)
    return AppConfig(**parsed)
  
config = fetch_config_from_yaml()

if __name__=="__main__":
  print(config)