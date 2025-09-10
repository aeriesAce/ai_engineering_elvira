from .constants import PATH
from pprint import pprint
from pydantic import BaseModel, Field
import json

def read_json(filename: str):
    with open(PATH / filename, "r") as file:
        data = json.load(file)
    return data

class Glossary(BaseModel):
    id: int
    word: str
    meaning: str

class GlossaryList(BaseModel):
    glossary: list[Glossary]

def glossary_data(filename):
    json_data = read_json(filename)
    wrapped_list = {"glossary": json_data}
    return GlossaryList.model_validate(wrapped_list)

if __name__ == "__main__":
    data = glossary_data("fastapi_glossary.json")
    pprint(data)