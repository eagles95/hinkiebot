from lib import ch
from nba import nbacommands
from nhl import nhlcommands

nbaprefix = "&"
nhlprefix = "#"

class HinkieBot(ch.RoomManager):
    def onConnect(self, room):
        print("Connected to "+room.name)
    
    def onReconnect(self, room):
        print("Reconnected to "+room.name)

    def onDisconnect(self, room):
        print("Disconnected from "+room.name)
        self.joinRoom(room.name)

    def onMessage(self, room, user, message):
        try:
            msg = message.body.encode("utf-8").lstrip()
            print(msg)
            if (msg[0] == nbaprefix):
                msg = msg[1:]
                try:
                    command,args = msg.split(" ",1)
                    print("command: " + command)
                    print("args: " + args)
                    ret = nbacommands.runCommand(command.lower(),args)
                except:
                    ret = nbacommands.runCommand(msg.lower(),None)
                if(ret!=None):
                    room.message(str(ret))
            elif(msg[0] == nhlprefix):
                msg = msg[1:]
                try:
                    command,args = msg.split(" ",1)
                    print("command: " + command)
                    print("args: " + args)
                    ret = nhlcommands.runCommand(command.lower(),args.lower())
                except:
                    ret = nhlcommands.runCommand(msg.lower(),None)
                if(ret!=None):
                    room.message(str(ret))
        except Exception as e:
            print(str(e))
rooms = ["hinkiebottesterxd","acleenba","csnphilly","nbcsphilly"]
bot_name = "HinkieBot"
bot_pw = "fuckthecowboys"
HinkieBot.easy_start(rooms,bot_name,bot_pw)
