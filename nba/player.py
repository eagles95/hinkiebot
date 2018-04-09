import json
import time
import urllib
import constants
import game
from datetime import datetime
from datetime import date
from operator import itemgetter

class PlayerNotFoundException(Exception):
        pass
"""
getPlayerID
"""
def getPlayerID(firstN,lastN=None):
    data = constants.player_data["league"]["standard"]
    if(lastN == None):
        for i in range(0,len(data)):
            if(data[i]["firstName"].lower() == firstN.lower() or data[i]["lastName"].lower() == firstN.lower()):
                return data[i]
        raise PlayerNotFoundException
    else:
        for i in range(0,len(data)):
            if(data[i]["firstName"].lower() == firstN.lower() and data[i]["lastName"].lower() == lastN.lower()):
                return data[i]
        raise PlayerNotFoundException

def getPlayerSummary(player):
	return player["firstName"] + " " + player["lastName"] + "(" + constants.id_to_team_name[int(player["teamId"])] + ") "

def getPlayerLast3(fName,lName):
    try:
        player = getPlayerID(fName,lName)
    except:
        return "Player name not found"
    playerID = player["personId"]
    url = "http://data.nba.net/data/10s/prod/v1/" + str(constants.SEASON_YEAR) +  "/players/" + str(playerID) + "_gamelog.json"
    response = urllib.urlopen(url)
    data =  json.loads(response.read())["league"]["standard"]
    ret = getPlayerSummary(player)
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
    try:
        player = getPlayerID(fName,lName)
    except:
        return("Player name not found")
    playerID = player["personId"]
    url = "http://data.nba.net/data/10s/prod/v1/" + str(constants.SEASON_YEAR) +  "/players/" + str(playerID) + "_profile.json"
    response = urllib.urlopen(url)
    data =  json.loads(response.read())["league"]["standard"]["stats"]["latest"]
    summary = getPlayerSummary(player)
    return summary + data["ppg"] + " ppg / " + data["apg"] + " apg / " + data["rpg"] + " rpg / " + data["bpg"] + " bpg / " + data["spg"] + " spg; " + data["fgp"] + " FG% / " + data["tpp"] + " 3PT% / " + data["ftp"] + " FT%"

def getPlayerLiveStats(fName,lName):
    try:
        player = getPlayerID(fName,lName)
    except:
        return "Player name not found"
    boxscore = game.getBoxScore(int(player["teamId"]))
    activePlayers = boxscore["stats"]["activePlayers"]
    ret = ""
    for i in range(0,len(activePlayers)):
        if(activePlayers[i]["personId"] == player["personId"]):
            ret =  getPlayerSummary(player)
            if (boxscore["basicGameData"]["hTeam"]["teamId"] == player["teamId"]):
                ret += "vs " + constants.id_to_team_name[int(boxscore["basicGameData"]["vTeam"]["teamId"])] + ", "
            else:
                ret += "@ " + constants.id_to_team_name[int(boxscore["basicGameData"]["hTeam"]["teamId"])] + ", "
            stats= activePlayers[i]
            ret += stats["points"] + "pts (" + stats["fgm"] + "/" + stats["fga"] + ")FGS ; "
            ret += stats["tpm"] + "/" + stats["tpa"] + " 3PT" + "; "
            ret += stats["ftm"] + "/" + stats["fta"] + " FT" + "; "
            ret += stats["assists"] + " AST; " + stats["totReb"] + " REB; " + stats["blocks"] + " BLK; "
            ret += stats["steals"] + " STL; " + stats["turnovers"] + " TO; " + stats["plusMinus"] + " +/-; " + stats["pFouls"] + " fouls"
            return ret + " in " + stats["min"] + " mins"
    return player["firstName"] + " " + player["lastName"] + " is inactive for the current " + constants.id_to_team_name[int(player["teamId"])] + " game"

def getRemain(flag,stat):
    if(flag == True):
        return stat
    elif(stat >= 10):
        return 0
    else:
        return (10 - stat)

def tripDubWatch(fName,lName):
    try:
        player = getPlayerID(fName,lName)
    except:
        return "Player name not found"
    boxscore = game.getBoxScore(int(player["teamId"]))
    activePlayers = boxscore["stats"]["activePlayers"]
    ret = ""
    tail = ""
    for i in range(0,len(activePlayers)):
        if(activePlayers[i]["personId"] == player["personId"]):
            stats = activePlayers[i]
            ret = getPlayerSummary(player)
            triple_double = [("pts",int(stats["points"])),("ast",int(stats["assists"])),("blk",int(stats["blocks"])),("stl",int(stats["steals"])),("reb",int(stats["totReb"]))]
            triple_double.sort(key=itemgetter(1),reverse=True)
            flag = False
            if(triple_double[2][1] >= 10):
                ret += "HAS COMPLETED A TRIPLE DOUBLE: "
                flag = True
            elif(boxscore["basicGameData"]["statusNum"] == constants.GAME_STATUS_FINAL):
                ret += "did not finish the game with a triple double: "
                flag = True
            else:
                ret += "still needs: "
                tail = " for a triple double"
            stat_strings = []
            for k in range(3):
                stat_pair = triple_double[k]
                if flag or stat_pair[1] < 10 :
                    stat_strings.append(str(getRemain(flag,stat_pair[1])) + stat_pair[0])
            ret += ", ".join(stat_strings)
            ret += tail
            if (boxscore["basicGameData"]["hTeam"]["teamId"] == player["teamId"]):
                ret += " (vs " + constants.id_to_team_name[int(boxscore["basicGameData"]["vTeam"]["teamId"])] + ")"
            else:
                ret += " (@ " + constants.id_to_team_name[int(boxscore["basicGameData"]["hTeam"]["teamId"])] + ")"
    if (ret == ""):
        ret = player["firstName"] + " " + player["lastName"] + " is inactive for the current " + constants.id_to_team_name[int(player["teamId"])] + " game"
    return ret

def calculate_age(birth):
    born = datetime.strptime(birth, '%Y-%m-%d').date()
    today = date.today()
    return str(today.year - born.year - ((today.month, today.day) < (born.month, born.day)))


def getProfile(fName,lName):
    try:
        player = getPlayerID(fName,lName)
    except:
        return "Player name not found"
    photourl = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/"+player["teamId"]+"/"+constants.SEASON_YEAR+"/260x190/"+player["personId"] + ".png"
    profile = getPlayerSummary(player) + "#" + player["jersey"] + ", " + player["pos"] + ", " + player["heightFeet"] + "'" + player["heightInches"] + "'', "+ player["weightPounds"] + ", age " + calculate_age(player["dateOfBirthUTC"])
    return photourl + " " + profile
