import requests
import json
import constants
import game


class PlayerNotFoundException(Exception):
            pass


def isGoalie(pos):
    if(pos == "G"):
        return True
    else:
        return False

def getPlayerSummary(player,flag):
    if(flag):
        team = player["playerTeamsPlayedFor"].split(",")[-1]
    else:
        team = player["playerTeamsPlayedFor"]
    return player["playerName"] + "(" + player["playerPositionCode"] + "/" + team + ") "

def getPlayerTeam(playerID):
    url = "http://statsapi.web.nhl.com/api/v1/people/" + str(playerID)
    return  requests.get(url).json()["people"][0]["currentTeam"]["id"]

def getPlayer(fName,lName):
    if(lName != None):
        #see if in players
        for i in range(0,constants.player_data["total"]):
            if(constants.player_data["data"][i]["playerFirstName"].lower() == fName and constants.player_data["data"][i]["playerLastName"].lower() == lName):
                return constants.player_data["data"][i]
        #see if goalie
        for i in range(0,constants.goalie_data["total"]):
            if(constants.goalie_data["data"][i]["playerFirstName"].lower() == fName and constants.goalie_data["data"][i]["playerLastName"].lower() == lName):
                return constants.goalie_data["data"][i]
    else:
        #look for a single name
        #see if in player
        for i in range(0,constants.player_data["total"]):
            if(constants.player_data["data"][i]["playerFirstName"].lower() == fName or constants.player_data["data"][i]["playerLastName"].lower() == fName):
                return constants.player_data["data"][i]
        #see if goalie
        for i in range(0,constants.goalie_data["total"]):
            if(constants.goalie_data["data"][i]["playerFirstName"].lower() == fName or constants.goalie_data["data"][i]["playerLastName"].lower() == fName):
                return constants.goalie_data["data"][i]
    #name not found
    raise PlayerNotFoundException


def getPlayerStats(fName,lName):
    print("stats command")
    try:
        player = getPlayer(fName,lName)
    except:
        return "Player Name not found :("
    ret =  getPlayerSummary(player,False)
    if(isGoalie(player["playerPositionCode"])):
        ret += str(player["wins"]) + "-" + str(player["losses"]) + "-" + str(player["otLosses"]) + " W-L-OT; "
        ret += str(player["savePctg"]) + " SV%; " + str(player["goalsAgainstAverage"]) + " GAA; "
        ret += str(player["shutouts"]) + " SO"
        return ret
    else:
        ret += str(player["goals"]) + " G; " + str(player["assists"]) + " A; " + str(player["points"]) + " PTs; "
        ret += str(player["shootingPctg"]) + " S%; " + str(player["plusMinus"]) + " +/-; "
        ret += str(round(player["timeOnIcePerGame"]/60,2)) + " TOIPerGame"
        return ret


def filterOutPlayer(players,player):
    if(isGoalie(player["playerPositionCode"])):
        return players["ID"+str(player["playerId"])]["stats"]["goalieStats"]
    else:
        return players["ID"+str(player["playerId"])]["stats"]["skaterStats"]

def getPlayerLiveStats(fName,lName):
    try:
        player = getPlayer(fName,lName)
    except:
        return "Player Name not found :("

    teamID = getPlayerTeam(player["playerId"])
    boxscore = game.getBoxscore(teamID)

    ret = getPlayerSummary(player,True)

    if(boxscore["home"]["team"]["id"] == teamID): 
        stats = filterOutPlayer(boxscore["home"]["players"],player)
        complement = "vs " + boxscore["away"]["team"]["name"]
    else:
        stats = filterOutPlayer(boxscore["away"]["players"],player)
        complement = "@ " + boxscore["home"]["team"]["name"]
    ret += complement + ": "
    
    if(isGoalie(player["playerPositionCode"])):
        ret += str(stats["shots"]) + "Shots; " + str(stats["saves"]) + "Saves; " 
        ret += str(round(stats["savePercentage"],2)) + " Sv%; "
    else:
        ret += str(stats["shots"]) + " S; " + str(stats["goals"]) + " G; " + str(stats["assists"]) + " A; "
        ret += str(stats["blocked"]) + " Blks; " + str(stats["hits"]) + " Hits; "
    ret += stats["timeOnIce"] + " TOI"
    return ret
