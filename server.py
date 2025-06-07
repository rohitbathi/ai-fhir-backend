from flask import Flask, request, jsonify
from main import parse_query, build_fhir_request

app = Flask(__name__)

PATIENTS = [
    {"name": "Alice", "age": 55, "gender": "female", "condition": "diabetes"},
    {"name": "Bob", "age": 60, "gender": "male", "condition": "hypertension"},
    {"name": "Carol", "age": 35, "gender": "female", "condition": "asthma"},
    {"name": "Dave", "age": 70, "gender": "male", "condition": "diabetes"},
]

def filter_patients(age_gt, conditions, gender):
    results = PATIENTS
    if age_gt is not None:
        results = [p for p in results if p["age"] > age_gt]
    if gender:
        results = [p for p in results if p["gender"] == gender]
    if conditions:
        results = [p for p in results if p["condition"] in conditions]
    return results

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json(force=True)
    text = data.get('text', '')
    age_gt, conditions, gender = parse_query(text)
    fhir_request = build_fhir_request(age_gt, conditions, gender)
    patients = filter_patients(age_gt, conditions, gender)
    return jsonify({'fhir_request': fhir_request, 'patients': patients})

if __name__ == '__main__':
    app.run(debug=True)
