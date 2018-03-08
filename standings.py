import json
import time
import datetime
import urllib
import pytz
import inflect
import constants

infl = inflect.engine()

def loadStanConf(conf):
    url = "http://data.nba.net/data/10s/prod/v1/current/standings_conference.json"
    response = urllib.urlopen(url)
    data = json.loads(response.read())["league"]["standard"]["conference"]
    if (conf == "west"):
        return data[conf]
    else:
        return data["east"]

def loadStanDiv(div):
    url = "http://data.nba.net/data/10s/prod/v1/current/standings_division.json"
    response = urllib.urlopen(url)
    data = json.loads(response.read())["league"]["standard"]["conference"]
    if (div in constants.WEST_CONF):
         return data["west"][div]
    else:
        return data["east"][div]


def loadStandAll():
    url = "http://data.nba.net/data/10s/prod/v1/current/standings_all.json"
    response = urllib.urlopen(url)
    return json.loads(response.read())["league"]["standard"]["teams"]




def confStandings(conf,n):
    data = loadStanConf(conf)
    ret = ""
    for i in range(0,n):
        ret = ret  + str(i+1) + ". " + constants.id_to_team_name[int(data[i]["teamId"])] + " (" + data[i]["win"] + "-" + data[i]["loss"] + ") / "
    return ret

def divStandings(div):
    data = loadStanDiv(div)
    ret = ""
    for i in range(0,5):
        ret = ret  + str(i+1) + ". " + constants.id_to_team_name[int(data[i]["teamId"])] + " (" + data[i]["win"] + "-" + data[i]["loss"] + ") / "
    return ret

def tankStandings(n):
    data = loadStandAll()
    ret = ""
    for i in range(1,n+1):
        ret = ret + str(i) + ". "+ constants.id_to_team_name[int(data[30-i]["teamId"])] + " (" + data[30-i]["win"] + "-" + data[i]["loss"] + ") /"
    return ret

def teamRecord(teamID):
    conf = constants.id_to_team_conf[teamID]
    data = loadStanConf(conf)
    for i in range(0,15):
        if (teamID == int(data[i]["teamId"])):
            return constants.id_to_team_name[int(data[i]["teamId"])] + " (" + data[i]["win"] + "-" + data[i]["loss"] + "), "+ infl.ordinal(i+1) + " place in " + conf

def getStandings(args):
    print("standings command")
    if (args in ["west","east"] ):
        return confStandings(args,15)
    elif((args in constants.WEST_CONF) or (args in constants.EAST_CONF)):
        return divStandings(args)
    else:
        return tankStandings(10) 

