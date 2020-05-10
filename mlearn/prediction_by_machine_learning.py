import os.path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Set random seed 
RSEED = 100
# Read the data
data = pd.read_csv(os.path.join(os.path.dirname(__file__), "../mlearn/needtaxi_logs.csv"))

# Remove latitude and longtiude outliers
data = data.loc[data['pickup_latitude'].between(40, 42)]
data = data.loc[data['pickup_longitude'].between(28, 30)]
data = data.loc[data['dropoff_latitude'].between(40, 42)]
data = data.loc[data['dropoff_longitude'].between(28, 30)]

# Absolute difference in latitude and longitude
data['abs_lat_diff'] = abs((data['dropoff_latitude'] - data['pickup_latitude']))
data['abs_lon_diff'] = abs((data['dropoff_longitude'] - data['pickup_longitude']))


# training and predictiong by linear regression
def get_linear_regression_prediction(p_lat, p_lon, d_lat, d_lon, taxi_type):
    # Split data
    if taxi_type == 0:
        X_train, X_test, y_train, y_test = train_test_split(data, np.array(data['fare_yellow']),
                                                            test_size=0.25, random_state=RSEED)
    elif taxi_type == 1:
        X_train, X_test, y_train, y_test = train_test_split(data, np.array(data['fare_turquoise']),
                                                            test_size=0.25, random_state=RSEED)
    else:
        X_train, X_test, y_train, y_test = train_test_split(data, np.array(data['fare_luxury']),
                                                            test_size=0.25, random_state=RSEED)

    linear_regression = LinearRegression()
    linear_regression.fit(X_train[['abs_lat_diff', 'abs_lon_diff']], y_train)

    new_abs_lat_diff = abs((d_lat - p_lat))
    new_abs_lon_diff = abs((d_lon - p_lon))

    X_new = np.array([[new_abs_lat_diff, new_abs_lon_diff]])
    pred = linear_regression.predict(X_new)

    return round(pred[0], 2)


# training and predictiong by random forest
def get_random_forest_prediction(p_lat, p_lon, d_lat, d_lon, taxi_type):
    # Split data
    if taxi_type == 0:
        X_train, X_test, y_train, y_test = train_test_split(data, np.array(data['fare_yellow']),
                                                            test_size=0.25, random_state=RSEED)
    elif taxi_type == 1:
        X_train, X_test, y_train, y_test = train_test_split(data, np.array(data['fare_turquoise']),
                                                            test_size=0.25, random_state=RSEED)
    else:
        X_train, X_test, y_train, y_test = train_test_split(data, np.array(data['fare_luxury']),
                                                            test_size=0.25, random_state=RSEED)

    random_forest = RandomForestRegressor(n_estimators=25, random_state=0)
    random_forest.fit(X_train[['abs_lat_diff', 'abs_lon_diff']], y_train)

    new_abs_lat_diff = abs((d_lat - p_lat))
    new_abs_lon_diff = abs((d_lon - p_lon))

    X_new = np.array([[new_abs_lat_diff, new_abs_lon_diff]])
    pred = random_forest.predict(X_new)

    return round(pred[0], 2)
