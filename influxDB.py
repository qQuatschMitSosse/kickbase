import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision, client
from influxdb_client.client.write_api import SYNCHRONOUS
import kickbaseScraper

#You have to start your local instance from influx db with the command influxd

token= "uIzahxzGkbd90lJ32JJj5gIHae3Zg5FxGflwyXEU5lhI_x-ErzJsvEwg_0f7Wo_coD6YVP3IdRefZ1mlJP8UHQ==";
org = "Kickbase"
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

def writeMarketValues(write_api,players):
    bucket = "market"
    for player in players:
        p= influxdb_client.Point("marketValue").tag("_id", player._id).tag("lastname", player.lastname).field("euro", player.marketValue)
        write_api.write(bucket=bucket, org=org, record=p)
def writePlayerStatus(write_api,players):
    bucket = "playerStatus"
    for player in players:
        p = influxdb_client.Point("playerStatus").tag("_id", player._id).tag("lastname", player.lastname).field("status",1)
        write_api.write(bucket=bucket, org=org, record=p)
def writePlayerMarketTrend(write_api,players):
    bucket = "marketTrend"
    for player in players:
        p = influxdb_client.Point("marketTrend").tag("_id", player._id).tag("lastname", player.lastname).field(
            "status", player.marketTrend)
        write_api.write(bucket=bucket, org=org, record=p)


#Queries the market value from an specific player over an specific time
#range is the days back for example last 7 days means (7, ...)
#playerName is the lastname of an specific Player
def getPlayerMarketValues(range, playerName):
    query = 'from(bucket: "market")\
            |> range(start: -{}d)\
            |> filter(fn: (r)=> r.lastname == "{}")'.format(range,playerName)

    results = []
    result = query_api.query(org=org,query=query)

    for table in result:
        for record in table.records:
            results.append((record.get_time(), record.get_value()))

    for eintrag in results:
        print("Datum: {} Marktwert: {}".format(eintrag[0],eintrag[1]))

def getMarketTrendByPlayer(range, playerName):
    query = 'from(bucket: "marketTrend")\
                |> range(start: -{}d)\
                |> filter(fn: (r)=> r.lastname == "{}")'.format(range, playerName)
    results = []
    result = query_api.query(org=org, query=query)

    for table in result:
        for record in table.records:
            results.append((record.get_time(), record.get_value()))

    for eintrag in results:
        print("Datum: {} MarketTrend: {}".format(eintrag[0], eintrag[1]))

#Kickbase update their marketValues daily at 9pm or 10pm  so we need to update the marketValues daily
def daylyRun():
    players = kickbaseScraper.getMarketValues()
    write_api = client.write_api(write_options=SYNCHRONOUS)
    writeMarketValues(write_api,players)
    writePlayerMarketTrend(write_api,players)


getPlayerMarketValues(3,"Vilhelmsson")
