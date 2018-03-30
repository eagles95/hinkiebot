import constants
import game
import player

def getInfo():
    return "List of commands here : https://hinkiebot.herokuapp.com/commands"

#COMMANDS
team_commands = {"score" : game.getScore}
player_commands = {"stats" : player.getPlayerStats, "livestats" : player.getPlayerLiveStats}
misc_commands = {"info" : getInfo, "commands" : getInfo}

def runCommand(command,args):
    if(args == None):
        if(command in misc_commands):
            return misc_commands[command]()
    else:
        if(command in team_commands):
            return team_commands[command](constants.team_name_to_id[args.lower()])
        elif(command in player_commands):
            try:
                firstName,lastName = args.split(" ",1)
                return player_commands[command](firstName,lastName)
            except:
                print("pls")
                return player_commands[command](args,None)
        else:
            return None
