from flask import Flask, jsonify
from IdMatcherPredictor import IDMatcher

app = Flask('__name__')


url1 = 'https://github.com/chris1610/pbpython/raw/master/data/hospital_account_info.csv'
url2 = 'https://raw.githubusercontent.com/chris1610/pbpython/master/data/hospital_reimbursement.csv'

@app.route('/api/v1/predict', methods=['GET'])
def predict():
    try:
        matcher = IDMatcher("State", "Provider State")

        dfA = matcher.read_data(url1)
        dfB = matcher.read_data(url2)
        prediction = matcher.predict_id_matches(dfA, dfB, 0.85)
        pred = prediction.to_json()
        return jsonify({
            'status': 'success',
            'data': pred
        }), 200
    except ValueError:
        return jsonify({
            'status': 'error',
            'message': ""
        }), 200




if __name__ == '__main__':
    app.run(debug=True)
