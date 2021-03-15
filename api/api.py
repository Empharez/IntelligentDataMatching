from flask import Flask, jsonify, request
from IdMatcherPredictor import IDMatcher
import json

app = Flask('__name__')


@app.route('/')
def home():
    return "Hello world"


@app.route('/predict', methods=['GET'])
def predict():
    matcher = IDMatcher("State", "Provider State")
    url = 'https://github.com/chris1610/pbpython/raw/master/data/hospital_account_info.csv'
    data = matcher.read_data(url).to_json()
    print("data", data)
    j_data = json.load(data)
    return j_data


if __name__ == '__main__':
    app.run(debug=True)
