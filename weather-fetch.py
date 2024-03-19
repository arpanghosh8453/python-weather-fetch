import os, time, sys, re, json, schedule, requests, logging
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError


INFLUXDB_HOST = os.environ.get("INFLUXDB_HOST") or 'localhost'
INFLUXDB_PORT = os.environ.get("INFLUXDB_PORT") or 8086
INFLUXDB_USERNAME = os.environ.get("INFLUXDB_USERNAME") or 'influxdb_username'
INFLUXDB_PASSWORD = os.environ.get("INFLUXDB_PASSWORD") or 'influxdb_password'
INFLUXDB_DATABASE = os.environ.get("INFLUXDB_DATABASE") or 'weather'
INFLUXDB_PLACE_TAG = os.environ.get("INFLUXDB_PLACE_TAG") or 'Hamilton'
FETCH_EVERY_N_MINUTES = int(os.environ.get("FETCH_EVERY_N_MINUTES")) or 15
PIRATEWEATHER_API_KEY = os.environ.get("PIRATEWEATHER_API_KEY") or ""
PIRATEWEATHER_LATITUDE = os.environ.get("PIRATEWEATHER_LATITUDE") or ""
PIRATEWEATHER_LONGITUDE = os.environ.get("PIRATEWEATHER_LONGITUDE") or ""
PIRATEWEATHER_UNIT = os.environ.get("PIRATEWEATHER_UNIT") or "ca"
PIRATEWEATHER_TZ = os.environ.get("PIRATEWEATHER_TZ") or "America/Toronto"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def fetch_weather():

    request_url = "https://api.pirateweather.net/forecast/" + str(PIRATEWEATHER_API_KEY) + "/" + str(PIRATEWEATHER_LATITUDE) + "," + str(PIRATEWEATHER_LONGITUDE) 
    weather_data = requests.get(request_url, params={'exclude':'alerts,minutely,hourly,daily', 'units': PIRATEWEATHER_UNIT, 'tz':PIRATEWEATHER_TZ}).json()

    filtered_weather_data = [
        {
            "measurement" : "current",
            "tags" : {
                "place": INFLUXDB_PLACE_TAG
            },
            "fields" : weather_data['currently']
        }
    ]

    client = InfluxDBClient(INFLUXDB_HOST, INFLUXDB_PORT, INFLUXDB_USERNAME, INFLUXDB_PASSWORD, INFLUXDB_DATABASE)

    try:
        logging.info("Result : " + str(filtered_weather_data))
        client.write_points(filtered_weather_data)
        logging.info("Success: Transfered data points to influxdb")
    except InfluxDBClientError as err:
        logging.error("Influxdb connection failed! " + str(err))

print("Starting Weather-Fetch....")
fetch_weather()
schedule.every(FETCH_EVERY_N_MINUTES).minutes.do(fetch_weather)

while True:
    schedule.run_pending()
    time.sleep(5)