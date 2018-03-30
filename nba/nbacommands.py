import game
import player
import standings
import scoreboard
import constants
from random import randint

def getHinkieQuote():
    return constants.hinkie_quotes[randint(0,len(constants.hinkie_quotes)-1)]

def getInfo():
	return "list of commands here : https://hinkiebot.herokuapp.com/commands"

def runCommand(command,args):
        if(args == None):
            if(command in scoreboard_commands):
                return scoreboard_commands[command]()
            elif(command in misc_commands):
                return misc_commands[command]()
        else:
            args = args.lower()
            if(command in team_commands):
                return team_commands[command](int(constants.teams_names[args]))
            elif(command in standings_commands):
                return standings_commands[command](constants.conf_names[args])
            elif(command in player_commands):
                if(args == "egg"):
                    return "Miss me with that egg shit fam"
                elif(args == "goat"):
                    return "28/43, 373yds, 3TD, 1 recyds, 1 recTD, SBLII MVP"
                else:
                    try:
                        firstName,lastName = args.split(" ",1)
                        return player_commands[command](firstName,lastName)
                    except:
                        return player_commands[command](args,None)
            else:
                return None

team_commands = {"score" : game.getGameScore,
                "nextgame" : game.getNextGame,
                "last5" : game.getLast5,
                "record": standings.teamRecord,
                "teamstats" : game.getTeamStats
}

standings_commands = {"standings" : standings.getStandings}

scoreboard_commands = {"scoreboard" : scoreboard.getScoreboard}

player_commands = {"recent" : player.getPlayerLast3,
                   "stats" : player.getPlayerStats,
                   "livestats" : player.getPlayerLiveStats,
                   "profile" : player.getProfile,
                    "tdalert" : player.tripDubWatch
}

misc_commands = {"quote": getHinkieQuote,"info" : getInfo,"commands" : getInfo}
