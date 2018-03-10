from lib import ch
import commands

prefix = "&"

class HinkieBot(ch.RoomManager):
    def onConnect(self, room):
        print("Connected to "+room.name)
    
    def onReconnect(self, room):
        print("Reconnected to "+room.name)

    def onDisconnect(self, room):
        print("Disconnected from "+room.name)

    def onMessage(self, room, user, message):
        msg = str(message.body).lstrip()
        print(msg)
        if (msg[0] == prefix):
            msg = msg[1:]
            try:
                command,args = msg.split(" ",1)
                print("command" + command)
                print("args" + args)
                ret = commands.runCommand(command,args)
            except:
                ret = commands.runCommand(msg,None)
            if(ret!=None):
                room.message(str(ret))



rooms = ["hinkiebottesterxd"]
bot_name = "HinkieBot"
bot_pw = "fuckthecowboys"
HinkieBot.easy_start(rooms,bot_name,bot_pw)
