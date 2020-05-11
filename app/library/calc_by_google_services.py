import os
import googlemaps

API_Key = os.getenv('GOOGLE_MAP_API_KEY')
gmaps = googlemaps.Client(key=API_Key)


# will be called from calc_by_latlng
def get_taxi_fare(distance, taxi_type):
    starting_fee = 5.0
    fare_per_100m = 0.31
    min_fare = 13.0

    # if taxi type is "yellow taxi"
    if taxi_type == 0:
        starting_fee = 5.0
        fare_per_100m = 0.31
        min_fare = 13.0

    # if taxi type is "turquoise taxi"
    elif taxi_type == 1:
        starting_fee = 5.75
        fare_per_100m = 0.36
        min_fare = 14.95

    # if taxi type is "luxury taxi"
    else:
        starting_fee = 8.5
        fare_per_100m = 0.53
        min_fare = 22.10

    taxi_fare = round(starting_fee + ((distance / 100) * fare_per_100m), 2)

    return taxi_fare if taxi_fare >= min_fare else min_fare


def calc_by_latlng(p_lat, p_lon, d_lat, d_lon, taxi_type):
    pickup_point = str(p_lat) + ', ' + str(p_lon)
    doff_point = str(d_lat) + ', ' + str(d_lon)

    distance = gmaps.distance_matrix(pickup_point, doff_point, mode="driving")["rows"][0]["elements"][0]["distance"][
        "value"]

    duration = gmaps.distance_matrix(pickup_point, doff_point, mode="driving")["rows"][0]["elements"][0]["duration"][
        "value"]

    taxi_fare = get_taxi_fare(distance, taxi_type)

    return {
        'distance': distance,
        'duration': duration,
        'taxi_fare': taxi_fare
    }
