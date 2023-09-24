import pymongo
import sys
import main
from constants import BUNDESLIGAIDS

try:
    client = pymongo.MongoClient("mongodb+srv://businesskurzmann:fQVSiklMVQbJRyLI@kickbase.did416a.mongodb.net/?retryWrites=true&w=majority")
    print("Connected")
except:
    print("Falsche URI")

database = client.kickbase

player_collection = database['playersV2']
try:
    for x in BUNDESLIGAIDS:
        player_collection.insert_many(main.getTeamDatabase(x))
except pymongo.errors.OperationFailure:
    print(
        "An authentication error was received. Are you sure your database user is authorized to perform write operations?")
    sys.exit(1)






