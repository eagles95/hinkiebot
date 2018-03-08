import json
import time
import urllib
import constants

from datetime import datetime


class PlayerNotFoundException(Exception):
        pass
"""
getPlayerID
"""
def getPlayerID(firstN,lastN=None):
    url = "http://data.nba.net/data/10s/prod/v1/" + constants.SEASON_YEAR  +"/players.json"
    response = urllib.urlopen(url)
    data = json.loads(response.read())["league"]["standard"]
    for i in range(0,len(data)):
        if(data[i]["firstName"].lower() == firstN.lower() and data[i]["lastName"].lower() == lastN.lower()):
            return data[i]
    raise PlayerNotFoundException

def getPlayerLast3(fName,lName):
    try:
        player = getPlayerID(fName,lName)
    except:
        return "Player name not found"
    playerID = player["personId"]
    url = "http://data.nba.net/data/10s/prod/v1/" + str(constants.SEASON_YEAR) +  "/players/" + str(playerID) + "_gamelog.json"
    response = urllib.urlopen(url)
    data =  json.loads(response.read())["league"]["standard"]
    ret = player["firstName"] + " " + player["lastName"] + "(" + constants.id_to_team_name[int(player["teamId"])] + ") " 
    for i in range(2,-1,-1):
        stats = data[i]["stats"]
        ret = ret + stats["points"] + " PTS/" +  stats["totReb"] + " REBS/" + stats["assists"] + " AST "
        if(data[i]["isHomeGame"]):
            if(data[i]["hTeam"]["isWinner"]):
                WL = "W"
            else:
                WL = "L"
            ret = ret + "in " + WL + " vs " + str(constants.id_to_team_name[int(data[i]["vTeam"]["teamId"])]) + "; "
        else:
            if(data[i]["vTeam"]["isWinner"]):
                WL = "W"
            else:
                WL = "L"
            ret = ret + "in " + WL + " @ " + str(constants.id_to_team_name[int(data[i]["hTeam"]["teamId"])]) + "; "
    return ret

def getPlayerStats(fName,lName):
    player = getPlayerID(fName,lName)
    playerID = player["personId"]
    url = "http://data.nba.net/data/10s/prod/v1/" + str(constants.SEASON_YEAR) +  "/players/" + str(playerID) + "_profile.json"
    response = urllib.urlopen(url)
    data =  json.loads(response.read())["league"]["standard"]["stats"]["latest"]
    return player["firstName"] + " " + player["lastName"] + "(" + constants.id_to_team_name[int(player["teamId"])] + ") "+ data["ppg"] + " ppg / " + data["apg"] + " apg / " + data["rpg"] + " rpg / " + data["bpg"] + " bpg / " + data["spg"] + " spg; " + data["fgp"] + " FG% / " + data["tpp"] + " 3PT% / " + data["ftp"] + " FT%" 


print(getPlayerLast3("ben","SIMMONS"))
print(getPlayerStats("JoEl","EmbiiD"))
