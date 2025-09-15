import pandas as pd
from .constants import DATA_PATH
import json

df = pd.read_excel(DATA_PATH / "resultat-ansokningsomgang-2024(2).xlsx", sheet_name = 4, skiprows = 5)

class Results:
    def __init__(self, limit=100):
        self._df = df.head(limit)
        self._df_full = df

    @property
    def df(self):
        return self._df
    
    def filter_school(self, school: str):
        mask = self._df_full["Utbildningsanordnare administrativ enhet"].str.casefold() == school.casefold()
        self._df = self._df_full[mask]
        return self
    
    def json_response(self):
        json_data = self.df.to_json(orient = "records")
        return json.loads(json_data)