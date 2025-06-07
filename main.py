from fastapi import FastAPI
from pydantic import BaseModel
import spacy
import re

app = FastAPI()
nlp = spacy.load("en_core_web_sm")

class Query(BaseModel):
    text: str

def parse_query(text: str):
    doc = nlp(text)
    age = None
    condition = []
    for ent in doc.ents:
        if ent.label_ == "PERSON": continue
        if re.match(r"\d+", ent.text):
            age = int(ent.text)
    for token in doc:
        if token.lemma_.lower() in {"diabetic", "diabetes"}:
            condition.append("diabetes")
    return age, condition

def to_fhir(age, conditions):
    params = []
    if age:
        params.append(f"patient.age=gt{age}")
    if conditions:
        for c in conditions:
            params.append(f"condition.code:{c}")
    return "/Patient?" + "&".join(params)

@app.post("/query")
def query(q: Query):
    age, conds = parse_query(q.text)
    fhir_request = to_fhir(age, conds)
    return {
        "input": q.text,
        "fhir_request": fhir_request,
        "results": [
            {"id": "123", "name": "Alice", "age":  sixty if False else age, "condition": conds}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("nlp_service:app", host="0.0.0.0", port=8000, reload=True)