import pandas as pd
from .constants import DATA_PATH
import json

df = pd.read_excel(DATA_PATH / "resultat-ansokningsomgang-2024(2).xlsx", sheet_name = "Tabell 3", header = 5)

class Results:
    def __init__(self, limit=100):
        self._df_full = df
        self._df = df.head(limit)
    
    def filter_school(self, school: str):
        mask = self._df_full["Utbildningsanordnare administrativ enhet"].str.casefold() == school.casefold()
        self._df = self._df_full[mask]
        return self
    
    def filter_fields(self, filter_: str):
        mask = self._df_full["Län"].str.casefold() == filter_.casefold()
        self._df = self._df_full[mask]
        return self
    
    def approved(self):
        mask = self._df_full["Beslut"].astype(str).str.strip().str.casefold() == "beviljad"
        self._df = self._df_full.loc[mask]
        return self
    
    def denied(self):
        mask = self._df_full["Beslut"].astype(str).str.strip().str.casefold() == "avslag"
        self._df = self._df_full.loc[mask]
        return self

    def json_response(self):
        json_data = self._df.to_json(orient = "records")
        return json.loads(json_data)