from kickbase_api.kickbase import Kickbase
from constants import NUTZERNAME,PASSWORD, BUNDESLIGAIDS
from player import influxPlayer, mongoDBPlayer

kickbase = Kickbase()
user, leagues = kickbase.login(NUTZERNAME,PASSWORD)

#This is my current league
league = kickbase.leagues()[2]



def getLineupSystem():
    print(kickbase.line_up(league).type)

def getLineup():
    print(kickbase.line_up(league).players)


# Funktion die eine Liste mit allen Market Values zurückgeben soll für die influxDB
def getMarketValues():
    marketValueList = []

    for id in BUNDESLIGAIDS:
        team = kickbase.team_players(id)
        for player in team:
            dbPlayer = influxPlayer(player.last_name, player.id, player.market_value, player.status, player.totalPoints,
                                    player.market_value_trend)
            marketValueList.append(dbPlayer)
    return marketValueList

def getTeamDatabase(teamId):
    team = kickbase.team_players(teamId)
    dbTeam = []

    for player in team:

        dbPlayer = mongoDBPlayer(player.id, player.first_name,player.last_name, player.team_id, player.position,
                                 player.status, player.average_points, player.totalPoints, player.market_value, player.market_value_trend, player.profile_big_path)
        dbTeam.append(dbPlayer)
    return dbTeam


def getAllPlayers():
    playerList = []
    for team in BUNDESLIGAIDS:
        players = getTeamDatabase(team)
        for player in players:
            playerList.append(player)
        playerList.append(players)
    return playerList

