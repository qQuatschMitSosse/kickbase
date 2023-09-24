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