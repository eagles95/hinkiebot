import json
import time
import datetime
import urllib
import pytz
import constants

"""
Returns the current gameID for that teamID
"""
def getGame(teamID):
    date = datetime.datetime.now(constants.TIME_ZONE).strftime('%Y%m%d')
    url = "http://data.nba.net/data/10s/prod/v1/" + date + "/scoreboard.json"
    response = urllib.urlopen(url)
    games = json.loads(response.read())["games"]
    for i in range(0,len(games)):
        if(((int(games[i]["vTeam"]["teamId"]) == teamID) or (int(games[i]["hTeam"]["teamId"] == teamID))) and (games[i]["statusNum"] == constants.GAME_STATUS_STARTED)):
            return games[i]

    #team not playing rn,need to get it from logs
    url = "http://data.nba.net/data/10s/prod/v1/" + constants.SEASON_YEAR + "/teams/" + constants.id_to_team_name[teamID].lower()  + "/schedule.json"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    lastGame = data["league"]["lastStandardGamePlayedIndex"]
    return data["league"]["standard"][lastGame]


"""
Returns the Score of the current game for that teamID
"""
def getGameScore(teamID):
    print("score method")
    game = getGame(teamID)
    ret = constants.id_to_team_name[int(game["vTeam"]["teamId"])] + " "  + game["vTeam"]["score"] + " @ " + constants.id_to_team_name[int(game["hTeam"]["teamId"])] + " "  + game["hTeam"]["score"]  
    if(game["statusNum"] == constants.GAME_STATUS_FINAL):
        return ret + str(', FINAL')
    elif (game["period"]["isHalftime"] == True):
        return ret + str(', HALF')
    else:
        ret =  ret + ", " + game["clock"] +" " 
        period = game["period"]["current"]
        if (period <= 4):
            return ret + "Q" + period
        else:
            return ret + "OT"


def getBoxScore(teamID):
    gm = getGame(teamID)
    url = "http://data.nba.net/data/10s/prod/v1/" + gm["startDateEastern"] +"/" + gm["gameId"]+ "_boxscore.json"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data


def getTeamStats(teamID):
    boxscore = getBoxScore(teamID)
    stats = boxscore["stats"]
    hTeamId = boxscore["basicGameData"]["hTeam"]["teamId"]
    vTeamId =  boxscore["basicGameData"]["vTeam"]["teamId"]
    ret = constants.id_to_team_name[int(teamID)]
    if(int(hTeamId) == teamID):
        ret += " vs " + constants.id_to_team_name[int(vTeamId)] + ", "
        stats = stats["hTeam"]["totals"]
    else:
        ret += " @ " + constants.id_to_team_name[int(hTeamId)] + ", "
        stats = stats["vTeam"]["totals"]
    ret += stats["fgm"] + "/" + stats["fga"] + "FGS; "
    ret += stats["tpm"] + "/" + stats["tpa"] + " 3PT; "
    ret += stats["ftm"] + "/" + stats["fta"] + " FT; "
    ret += stats["assists"] + " AST; " + stats["defReb"] + " DEFREB; " + stats["offReb"] + " OFFREB; " + stats["totReb"] + " REB; " 
    ret += stats["blocks"] + " BLK; "
    ret += stats["steals"] + " STL; " + stats["turnovers"] + " TO"
    return ret


"""
Parse game date and time data and convert to EST timezone
"""
def getDatetime(dateTime):
    date = dateTime.split("T")[0]
    time = dateTime.split("T")[1].split(".")[0]
    dateTime = str(date) + str(" ") + str(time)
    dateTime = datetime.datetime.strptime( dateTime, '%Y-%m-%d %H:%M:%S')
    dateTime = dateTime.replace(tzinfo=pytz.utc).astimezone(constants.TIME_ZONE)
    return datetime.datetime.strptime( str(dateTime).rsplit('-',1)[0], '%Y-%m-%d %H:%M:%S').strftime("%m/%d/%Y %I:%M %p")
    


"""
Loads team schedule from data.nba.net
"""
def loadSched(teamID):
    url = "http://data.nba.net/data/10s/prod/v1/" + constants.SEASON_YEAR +  "/teams/" + str(constants.id_to_team_name[teamID].lower()) + "/schedule.json"
    response = urllib.urlopen(url)
    return json.loads(response.read())

"""
Get time,date and opponnent of next game
"""
def getNextGame(teamID):
    data = loadSched(teamID)
    lastGame = data["league"]["lastStandardGamePlayedIndex"]
    dateTime = getDatetime(data["league"]["standard"][lastGame+1]["startTimeUTC"]) + " ET"
    if (data["league"]["standard"][lastGame+1]["vTeam"]["teamId"] == str(teamID)):
        return constants.id_to_team_name[teamID] + " @ " + constants.id_to_team_name[int(data["league"]["standard"][lastGame+1]["hTeam"]["teamId"])] + ", " + dateTime
    else:
        return constants.id_to_team_name[int(data["league"]["standard"][lastGame+1]["vTeam"]["teamId"])] + " @ "+ constants.id_to_team_name[teamID] + ", " + dateTime



"""
Returns the results of teamID last 5 games
"""
def getLast5(teamID):
    data = loadSched(teamID)
    lastGame = data["league"]["lastStandardGamePlayedIndex"]
    ret = "Last 5 " + str(constants.id_to_team_name[teamID]) + " games: "
    for i in range(1,6):
        index = lastGame-(5-i)
        vTeamId =  data["league"]["standard"][index]["vTeam"]["teamId"]
        hTeamId = data["league"]["standard"][index]["hTeam"]["teamId"]
        vTeamScore = int(data["league"]["standard"][index]["vTeam"]["score"])
        hTeamScore = int(data["league"]["standard"][index]["hTeam"]["score"])
        if ( vTeamId == str(teamID)):
            #team is on the road
            ret = ret + "@ " + constants.id_to_team_name[int(hTeamId)]
            if (vTeamScore > hTeamScore):
                ret = ret + " W, " + str(vTeamScore) + " - " + str(hTeamScore) + "/ "
            else:
                ret = ret + " L, " + str(vTeamScore) + " - " + str(hTeamScore) + "/ "
        else:
            #team is at home
            ret = ret + "vs " + constants.id_to_team_name[int(data["league"]["standard"][index]["vTeam"]["teamId"])]
            if (vTeamScore < hTeamScore):
                ret = ret + " W, " + str(vTeamScore) + " - " + str(hTeamScore) + "/ "
            else:
                ret = ret + " L, " + str(vTeamScore) + " - " + str(hTeamScore) + "/ "

    return ret

print(getTeamStats(constants.DEN_TEAM_ID))
