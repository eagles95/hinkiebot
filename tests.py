import nba_py
import json
import constants
import time
import datetime
import urllib
import pytz
import constants

from nba_py import team
from nba_py import game
from nba_py import player

def getGameID(teamID):
    return nba_py.team.TeamGameLogs(teamID, season=constants.CURRENT_SEASON, season_type=constants.SEASON_TYPE).info()[0]['Game_ID']


def getGameScore(teamID):
    time.sleep(2)
    score = nba_py.game.BoxscoreSummary(getGameID(teamID)).line_score()
    ret =  str(score[1]['TEAM_CITY_NAME']) +str(' ') + str(score[1]['TEAM_NICKNAME']) +str(' ')+ str(score[1]['PTS']) + str(' @ ')+ str(score[0]['TEAM_CITY_NAME']) +str(' ') +str(score[0]['TEAM_NICKNAME']) +str(' ')+str(score[0]['PTS']    )  
    gametime = nba_py.game.BoxscoreSummary(getGameID(teamID)).game_summary()
    if(gametime[0]['GAME_STATUS_ID'] == constants.GAME_STATUS_FINAL):
        return ret + str(', FINAL')
    elif (gametime[0]['GAME_STATUS_TEXT'] == "Halftime"):
        return ret + str(', HALF')
    else:
        return ret + str(', ') + str(gametime[0]['LIVE_PERIOD_TIME_BCAST'].split("-")[0])




"""
for i in range(0,100):
    print(i)
    scoreboard = nba_py.Scoreboard(month=3, day=3, year=2018, league_id='00', offset=0).json['resultSets'][0]['rowSet']

print(json.dumps(scoreboard))

print(type(scoreboard))
print(len(scoreboard))
print(getGameID(constants.PHI_TEAM_ID))
print(getGameID(constants.CLE_TEAM_ID)) 
print(getGameID(constants.DEN_TEAM_ID))
print(getGameID(constants.ORL_TEAM_ID))
print(getGameID(constants.MEM_TEAM_ID))
print(getGameID(constants.BOS_TEAM_ID))

xd = nba_py.game.BoxscoreSummary(getGameID(constants.SAC_TEAM_ID)).line_score()
print(json.dumps(xd))
xd = nba_py.game.BoxscoreSummary(getGameID(constants.SAC_TEAM_ID)).game_summary()
print(json.dumps(xd))

print(getGameScore(constants.BOS_TEAM_ID))
print(getGameScore(constants.MEM_TEAM_ID))
print(getGameScore(constants.DEN_TEAM_ID))
print(getGameScore(constants.DET_TEAM_ID))
print(getGameScore(constants.LAL_TEAM_ID))
print(getGameScore(constants.OKC_TEAM_ID))
print(getGameScore(constants.SAC_TEAM_ID))
print(getGameScore(constants.PHI_TEAM_ID))
"""

"""
url = "http://data.nba.net/data/10s/prod/v1/2017/teams/sixers/schedule.json"
response = urllib.urlopen(url)
data = json.loads(response.read())
lastGame = data["league"]["lastStandardGamePlayedIndex"]
dateTime = data["league"]["standard"][lastGame+1]["startTimeUTC"]
date = dateTime.split("T")[0]
time = dateTime.split("T")[1].split(".")[0]
dateTime = str(date) + str(" ") + str(time)
print(dateTime)
datetime_obj = datetime.datetime.strptime( dateTime, '%Y-%m-%d %H:%M:%S')
print(datetime_obj)
local_dt = datetime_obj.replace(tzinfo=pytz.utc).astimezone(constants.TIME_ZONE)
print(local_dt.hour)






for i in range(0,100):
    print(i)
    scoreboard = nba_py.Scoreboard(month=3, day=3, year=2018, league_id='00', offset=0).json['resultSets'][0]['rowSet']

print(json.dumps(scoreboard))

print(type(scoreboard))
print(len(scoreboard))

print(getGameID(constants.PHI_TEAM_ID))
print(getGameID(constants.CLE_TEAM_ID)) 
print(getGameID(constants.DEN_TEAM_ID))
print(getGameID(constants.ORL_TEAM_ID))
print(getGameID(constants.MEM_TEAM_ID))
print(getGameID(constants.BOS_TEAM_ID))
xd = nba_py.game.BoxscoreSummary(getGameID(constants.SAC_TEAM_ID)).line_score()
print(json.dumps(xd))
xd = nba_py.game.BoxscoreSummary(getGameID(constants.SAC_TEAM_ID)).game_summary()
print(json.dumps(xd))

print(getGameScore(constants.BOS_TEAM_ID))
print(getGameScore(constants.MEM_TEAM_ID))
print(getGameScore(constants.DEN_TEAM_ID))
print(getGameScore(constants.DET_TEAM_ID))
print(getGameScore(constants.LAL_TEAM_ID))
print(getGameScore(constants.OKC_TEAM_ID))
print(getGameScore(constants.SAC_TEAM_ID))

url = "http://data.nba.net/data/10s/prod/v1/2017/teams/sixers/schedule.json"
response = urllib.urlopen(url)
data = json.loads(response.read())
lastGame = data["league"]["lastStandardGamePlayedIndex"]
for i in range(0,5):
    game = data["league"]["standard"][lastgame-(5-i)]
"""    
#print(json.dumps(nba_py.team.TeamDetails(constants.PHI_TEAM_ID).json))
print(json.dumps(nba_py.team.TeamList(league_id='00').json))


