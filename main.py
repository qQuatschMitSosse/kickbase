from kickbase_api.kickbase import Kickbase
from kickbase_api.exceptions import *
from kickbase_api.models import *
from constants import NUTZERNAME,PASSWORD, BUNDESLIGAIDS


kickbase = Kickbase()
user, leagues = kickbase.login(NUTZERNAME,PASSWORD)
league = kickbase.leagues()[2]


def getLineupSystem():
    print(kickbase.line_up(league).type)

def getLineup():
    print(kickbase.line_up(league).players)

class influxPlayer:
    def __init__(self,lastname,_id,marketValue,status,totalPoints,marketTrend):
        self.lastname=lastname
        self._id=_id
        self.marketValue=marketValue
        self.status=status
        self.totalPoints=totalPoints
        self.marketTrend=marketTrend

class mongoDBPlayer:
    def __init__(self,id, firstname, lastname, teamID, position, status, avgPoints, totalPoints,marketValue,
                 marketTrend, profilePictureBig):
        self._id = id
        self.firstname = firstname
        self.lastname = lastname
        self.teamID = teamID
        self.position = position
        self.status = status
        self.avgPoints= avgPoints
        self.totalPoints = totalPoints
        self.marketValue = marketValue
        self.marketTrend = marketValue
        self.profilePictureBig = profilePictureBig


#Funktion die eine Liste mit allen Market Values zurückgeben soll für die influxxDB 
def getMarketValues():
    marketValueList = []

    for id in BUNDESLIGAIDS:
        team = kickbase.team_players(id)
        for player in team:
            
            dbPlayer = influxPlayer(player.last_name, player.id, player.market_value,player.status,player.totalPoints,player.market_value_trend)
            marketValueList.append(dbPlayer)
    return marketValueList

#Funktion bekommt eine teamId übergeben (siehe constants.py)
#
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






