import json
import time
import pytz
from datetime import datetime,timedelta
import urllib
import constants


"""
load todays scoreboard from url
"""
def loadScoreboard():
    date = datetime.now(constants.TIME_ZONE)
    if (date.hour < constants.SCOREBOARD_UPDATE_HOUR):
        date =  date - timedelta(days=1)
    date = date.strftime('%Y%m%d')
    url = "http://data.nba.net/data/10s/prod/v1/" + date + "/scoreboard.json"
    response = urllib.urlopen(url)
    return json.loads(response.read())
    
"""
Get score or starting times for todays nba games
"""
def getScoreboard():
    print("scoreboard command")
    data = loadScoreboard()
    numGames = data["numGames"]
    if (numGames == 0):
        return "No games today"
    data = data["games"]
    ret = ""
    for i in range(0,numGames):
        hTeam = constants.id_to_team_name[int(data[i]["hTeam"]["teamId"])]
        vTeam = constants.id_to_team_name[int(data[i]["vTeam"]["teamId"])]
        hTeamScore = data[i]["hTeam"]["score"]
        vTeamScore = data[i]["vTeam"]["score"]
        gameStatus = data[i]["statusNum"]
        if(gameStatus == constants.GAME_STATUS_BEFORE):
            ret =  ret + vTeam + " @ " + hTeam + ", " + data[i]["startTimeEastern"] + "; "
        else:
            ret  = ret + vTeam + " " + vTeamScore + " @ " + hTeam + " " + hTeamScore + ", "
            if (gameStatus == constants.GAME_STATUS_FINAL):
                ret = ret + "FINAL" + "/    "
            else:
                period = data[i]["period"]["current"]
                if (period <= 4):
                    ret = ret + str(period) + "Q/    "
                else:
                    ret = ret + "OT" + str(period - 4) + "/    "

    return ret
