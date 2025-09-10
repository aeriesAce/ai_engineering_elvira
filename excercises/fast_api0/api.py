from fastapi import FastAPI
from .data_processing import glossary_data, Glossary

app = FastAPI()

gloss_list = glossary_data("fastapi_glossary.json")
glossaries = gloss_list.glossary

@app.get("/glossary")
async def read_glossary():
    return glossaries

@app.get("/glossary/word/{word}")
async def read_gloss_by_word(word: str):
    return [gloss for gloss in glossaries if gloss.word.casefold() == word.casefold()]

# filter out a specific word, query parameter
@app.get("/glossary/word")
async def find_specific_word(word: str):
    return [gloss for gloss in glossaries if gloss.word.casefold() == word.casefold()]

@app.post("/glossary/add_glossary")
async def add_glossary_word(gloss_request: Glossary):
    new_word = Glossary.model_validate(gloss_request)
    glossaries.append(new_word)

    return new_word

# update the glossary
@app.put("/glossary/update_glossary")
async def update_glossary(updated_glossary: Glossary):
    for i, gloss in enumerate(glossaries):
        if gloss.id == updated_glossary.id:
            gloss[i] = updated_glossary
    
    return updated_glossary

# remove a glossary
@app.delete("/glossary/delete_glossary/{id}")
async def delete_glossary(id: int):
    for i, gloss in enumerate(glossaries):
        if gloss.id == id:
            del glossaries[i]
            break