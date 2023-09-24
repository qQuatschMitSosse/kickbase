import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision, client
from influxdb_client.client.write_api import SYNCHRONOUS
import main

token= "uIzahxzGkbd90lJ32JJj5gIHae3Zg5FxGflwyXEU5lhI_x-ErzJsvEwg_0f7Wo_coD6YVP3IdRefZ1mlJP8UHQ==";
org = "Kickbase"
url = "http://localhost:8086"
bucket = "market"


client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()


def writeMarketValues():
    players = main.getMarketValues()
    write_api =client.write_api(write_options=SYNCHRONOUS)
    for player in players:
        p= influxdb_client.Point("marketValue").tag("_id", player._id).tag("lastname", player.lastname).field("euro", player.marketValue)
        print(p)
        write_api.write(bucket=bucket, org=org, record=p)


def getBiggestDifference():
    query = 'from(bucket: "market")\
            |> range(start: -2d)\
            |> filter(fn: (r)=> r.lastname == "Can")'

    result = query_api.query(org=org,query=query)
    output = result.to_values(columns=['id', '_time', 'lastname', 'marketValue'])
    print(output)
