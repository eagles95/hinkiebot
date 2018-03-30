import requests
import json
import constants

class PlayerNotFoundException(Exception):
            pass



def getPlayer(fName,lName):
    if(lName != None):
        #see if in players
        for i in range(0,constants.player_data["total"]):
            if(constants.player_data["data"][i]["playerFirstName"] == fName and constants.player_data["data"][i]["playerLastName"] == lName):
                return constants.player_data["data"][i]
        #see if goalie
        for i in range(0,constants.goalie_data["total"]):
            if(constants.goalie_data["data"][i]["playerFirstName"] == fName and constants.goalie_data["data"][i]["playerLastName"] == lName):
                return constants.goalie_data["data"][i]
    else:
        #look for a single name
        #see if in players
        for i in range(0,constants.player_data["total"]):
            if(constants.player_data["data"][i]["playerFirstName"] == fName or constants.player_data["data"][i]["playerLastName"] == fName):
                return constants.player_data["data"][i]
        #see if goalie
        for i in range(0,constants.goalie_data["total"]):
            if(constants.goalie_data["data"][i]["playerFirstName"] == fName or constants.goalie_data["data"][i]["playerLastName"] == fName):
                return constants.goalie_data["data"][i]
    #name not found
    raise PlayerNotFoundException
