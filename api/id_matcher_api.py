import datetime

import numpy as np
import pandas as pd
from cachetools import cached, TTLCache
from flask import Flask, jsonify
from sqlalchemy import create_engine

from IdMatcherPredictor import IDMatcher

app = Flask('__name__')

cache = TTLCache(maxsize=100, ttl=60)


@cached(cache)
def read_data():
    engine = create_engine("db_type+db_lib_sql-alchemy://username:password@host/SID")
    query = '''SELECT 
        id,
        first_name,
        last_name,
        email,
        phone_number,
        date_of_birth
        from remita_activation_request'''
    kpi_list = pd.read_sql(query, engine, index_col='id')
    print("data type", kpi_list.dtypes)
    kpi_records = pd.DataFrame(kpi_list)
    return kpi_records


kpi_records = read_data()

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
    predictions = matcher.find_possible_matches(payload, kpi_records, threshold)
    return jsonify({
        'status': 'success',
        'data': predictions
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
