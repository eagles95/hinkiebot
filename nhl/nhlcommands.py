import constants
import game
#COMMANDS
team_commands = {"score" : game.getScore}


def runCommand(command,args):
    if(command in team_commands):
        return team_commands[command](constants.team_name_to_id[args.lower()])
    else:
        return None
