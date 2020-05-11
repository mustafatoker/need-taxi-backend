from flask import Flask, jsonify, request
from kanpai import Kanpai
from app.config.settings import *
from app.library.calc_by_google_services import calc_by_latlng
from app.library.prediction_by_machine_learning import get_linear_regression_prediction, get_random_forest_prediction

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Need Taxi</h1>'''


@app.route('/api/v1/predict-fares', methods=['POST'])
def predictFares():
    schema = Kanpai.Object({
        "pickup_latitude": Kanpai.Number().required(),
        "pickup_longitude": Kanpai.Number().required(),
        "drop_off_latitude": Kanpai.Number().required(),
        "drop_off_longitude": Kanpai.Number().required(),
        "taxi_type": Kanpai.Number().required(),
    })

    validation_form_result = schema.validate(request.json)

    if validation_form_result.get('success', False) is False:
        return jsonify({
            "status": "Error",
            "errors": validation_form_result.get("error")
        })

    form_data = validation_form_result.get("data")

    p_latitude = form_data['pickup_latitude']
    p_longitude = form_data['pickup_longitude']
    d_latitude = form_data['drop_off_latitude']
    d_longitude = form_data['drop_off_longitude']
    taxi_type = form_data['taxi_type']

    random_forest_prediction = get_random_forest_prediction(
        p_latitude, p_longitude, d_latitude, d_longitude, taxi_type
    )

    linear_regression_prediction = get_linear_regression_prediction(
        p_latitude, p_longitude, d_latitude, d_longitude, taxi_type
    )

    return jsonify(
        random_forest_prediction=random_forest_prediction,
        linear_regression_prediction=linear_regression_prediction,
    )


@app.route('/api/v1/calculation-duration-distances', methods=['POST'])
def calculateDurationDistance():
    schema = Kanpai.Object({
        "pickup_latitude": Kanpai.Number().required(),
        "pickup_longitude": Kanpai.Number().required(),
        "drop_off_latitude": Kanpai.Number().required(),
        "drop_off_longitude": Kanpai.Number().required(),
        "taxi_type": Kanpai.Number().required(),
    })

    validation_form_result = schema.validate(request.json)

    if validation_form_result.get('success', False) is False:
        return jsonify({
            "status": "Error",
            "errors": validation_form_result.get("error")
        })

    form_data = validation_form_result.get("data")

    p_latitude = form_data['pickup_latitude']
    p_longitude = form_data['pickup_longitude']
    d_latitude = form_data['drop_off_latitude']
    d_longitude = form_data['drop_off_longitude']
    taxi_type = form_data['taxi_type']

    calculationOfDistances = calc_by_latlng(
        p_latitude, p_longitude, d_latitude, d_longitude, taxi_type
    )

    distance = str(calculationOfDistances['distance'] / 1000)
    duration = calculationOfDistances['duration']
    total_fee = calculationOfDistances['taxi_fare']

    return jsonify(
        distance=distance,
        duration=duration,
        totalFee=total_fee,
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
