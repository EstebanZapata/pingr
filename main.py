import os
import time
from datetime import datetime
from influxdb import InfluxDBClient
from pythonping import ping

target = os.environ.get('TARGET', '8.8.8.8')
wait = os.environ.get('WAIT', '1')

influxdbUser = os.environ.get('INFLUXDB_USER')
influxdbPassword = os.environ.get('INFLUXDB_USER_PASSWORD')
influxdbHost = os.environ.get('INFLUXDB_HOST', 'influxdb')
influxdbPort = os.environ.get('INFLUXDB_PORT', '8086')
influxdbDatabase = os.environ.get('INFLUXDB_DATABASE', 'internet-stats')

def initInflux():
    client = InfluxDBClient(host=influxdbHost, port=int(influxdbPort), username=influxdbUser, password=influxdbPassword)
    client.create_database(influxdbDatabase)
    client.switch_database(influxdbDatabase)
    return client
    
client = initInflux()

def handleResponse(response):
    if (influxdbUser is None or influxdbPassword is None):
        print(response)
    else:
        sendToInflux(response)
    
def sendToInflux(response):
    json = [{
        "measurement": "ping",
        "tags": {
            "target": target
        },
        "time": str(datetime.utcnow()),
        "fields": {
            "responseTimeMs": response.time_elapsed_ms if response.success else 9999
        }
    }]
    
    client.write_points(json)
    print('success write')

while True:
    responses = ping(target, timeout=1, count=1)
    for response in responses:
        handleResponse(response)
    time.sleep(int(wait))
