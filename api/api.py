from flask import Flask, jsonify
from IdMatcherPredictor import IDMatcher
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import datetime
"""
engine = create_engine("dbtype+lib://@username:@password@localhost/db_service")
query = '''SELECT 
    first_name,
    last_name,
    email,
    phone_number,
    date_of_birth
    from table_name'''
kpi_list = pd.read_sql(query, engine)
print("data type", kpi_list.dtypes)
kpi_records = pd.DataFrame(kpi_list)"""

kpi_record_job = pd.read_pickle('kpi_records.pkl')
app = Flask('__name__')

request_body = {
    'first_name': 'Akin',
    'last_name': 'Omolaja',
    'email': 'kinzojob@yahoo.com',
    'phone_number': '+2348023774433',
    'date_of_birth': np.datetime64(datetime.datetime(1985, 7, 10))
}

payload = pd.json_normalize(request_body)



@app.route('/api/v1/predict', methods=['GET'])
def predict():
    matcher = IDMatcher("date_of_birth", "date_of_birth")
    threshold = 0.85
    predictions = matcher.find_possible_matches(payload, kpi_record_job, threshold)
    return jsonify({
        'status': 'success',
        'data': predictions
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
