# AI FHIR Backend

This project contains a small example script that converts natural language
queries into simulated FHIR API requests. It uses `spaCy` to extract
simple entities like age, conditions and gender from the input text.

## Setup

Install the required dependency and download the spaCy model:

```bash
pip install spacy
python -m spacy download en_core_web_sm
```

## Running the script

Run the program and enter a query when prompted:

```bash
python main.py
```

The script prints a simulated FHIR `Patient` search request based on the
entities it finds in your query.

## Example mappings

| Input text                                   | FHIR request                                   |
|----------------------------------------------|------------------------------------------------|
| `Show me all diabetic patients over 50`      | `/Patient?age=gt50&condition.code=diabetes`    |
| `List hypertensive male patients over 40`    | `/Patient?age=gt40&gender=male&condition.code=hypertension` |
| `Asthmatic female patients over 30`          | `/Patient?age=gt30&gender=female&condition.code=asthma` |
| `Find male patients over 65 with diabetes`   | `/Patient?age=gt65&gender=male&condition.code=diabetes` |
| `Patients over 20 with asthma or hypertension` | `/Patient?age=gt20&condition.code=asthma&condition.code=hypertension` |
