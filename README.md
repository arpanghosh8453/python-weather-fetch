# python-weather-fetch
A script for pulling weather data from pirateweather API to influxdb

![Dashboard](https://github.com/arpanghosh8453/python-weather-fetch/blob/main/screenshot.png?raw=true)

Get an API token from here : https://pirate-weather.apiable.io/

Use the following docker compose. You must already have Influxdb setup and running

```
version: '3.4'
services:
  python-weather-fetch:
    restart: unless-stopped
    image: thisisarpanghosh/python-weather-fetch:latest
    container_name: python-weather-fetch
    environment:
      - INFLUXDB_HOST=influxdb
      - INFLUXDB_PORT=8086
      - INFLUXDB_USERNAME=influxdb_username
      - INFLUXDB_PASSWORD=influxdb_password
      - INFLUXDB_DATABASE=weather
      - INFLUXDB_PLACE_TAG=Hamilton
      - FETCH_EVERY_N_MINUTES=15
      - PIRATEWEATHER_API_KEY=your_API_key_here
      - PIRATEWEATHER_LATITUDE=yy.zz
      - PIRATEWEATHER_LONGITUDE=xx.yy
      - PIRATEWEATHER_UNIT=ca
      - PIRATEWEATHER_TZ=America/Toronto
networks:
  default:
    external: true
    name: proxy-network
```
