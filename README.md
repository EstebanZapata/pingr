docker build -t pingr:0.1 .

Env:
SOURCE: Source of ping (default blank)
TARGET: Target of ping (default 8.8.8.8)
WAIT: Seconds between pings (default 1)
PROVIDER: Internet provider (default blank)

INFLUXDB_USER
INFLUXDB_USER_PASSWORD
INFLUXDB_HOST: Host of influxdb (default influxdb)
INFLUXDB_PORT: Port of influxdb (default 8086)
INFLUXDB_DATABASE: Database of influxdb (default internet-stats)
