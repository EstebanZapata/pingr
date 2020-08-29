import os
import time
from datetime import datetime
from influxdb import InfluxDBClient
from pythonping import ping

source = os.environ.get('SOURCE', '')
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
    point = [{
        "measurement": "ping",
        "tags": {
            "source": source,
            "target": target
        },
        "time": str(datetime.utcnow()),
        "fields": {
            "responseTimeMs": response.time_elapsed_ms if response.success else 999,
            "success": response.success
        }
    }]
    
    client.write_points(point)
    print('Influx success: ' + str(response))

while True:
    responses = ping(target, timeout=1, count=1)
    for response in responses:
        handleResponse(response)
    time.sleep(int(wait))
