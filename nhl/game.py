import constants
import requests
import json

def getGame(teamID):
    #Check if team is playing rn
    url = "https://statsapi.web.nhl.com/api/v1/teams/"+str(teamID)+"?expand=team.schedule.next"
    data = requests.get(url).json()["teams"][0]["nextGameSchedule"]["dates"][0]["games"][0]
    if(data["status"]["statusCode"] != "1"):
        #team is playing, return this game
        return data
    else:
        #team not playing, return last game
        url = "https://statsapi.web.nhl.com/api/v1/teams/"+str(teamID)+"?expand=team.schedule.previous"
        data = requests.get(url).json()["teams"][0]["previousGameSchedule"]["dates"][0]["games"][0]
        return data


#Returns score of the latest game
def getScore(teamID):
    game = getGame(teamID)
    awayTeam = game["teams"]["away"]["team"]["name"] + " " + str(game["teams"]["away"]["score"])
    homeTeam = game["teams"]["home"]["team"]["name"] + " " + str(game["teams"]["home"]["score"])
    status = game["status"]["abstractGameState"]
    return awayTeam + " @ " + homeTeam + ", " + status


def getBoxscore(teamID):
    game = getGame(teamID)
    url = "https://statsapi.web.nhl.com/api/v1/game/"+str(game["gamePk"])+"/boxscore"
    data = requests.get(url).json()["teams"]
    return data 
