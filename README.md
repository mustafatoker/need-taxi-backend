# The Need Taxi Backend API
Predict taxi fares through machine learning using random forest and linear_regression.

#### Installation
```
- pip install -r requirements.txt
- set FLASK_APP=app.py - Windows
- export FLASK_APP=hello.py - Unix
- flask run
```

Running on http://127.0.0.1:5000/


#### Endpoints
```
HEAD | POST predict-fares
HEAD | POST calculation-duration-distances
```

You can see endpoint details in the postman collection.


#### Sample Request:

```
HEAD | POST http://127.0.0.1:5000/api/v1/predict-fares

Request Payload:
{
   "pickup_latitude" : 41.05,
   "pickup_longitude" : 28.98,
   "drop_off_latitude" : 41.14,
   "drop_off_longitude" : 28.46,
   "taxi_type" : 0
}

Response:
{
  "linear_regression_prediction": 186.66,
  "random_forest_prediction": 184.4
}
```

