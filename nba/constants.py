import datetime
import pytz
import requests
from apscheduler.scheduler import Scheduler

#Season Year
SEASON_YEAR = "2018"

#player data
player_url = "http://data.nba.net/data/10s/prod/v1/" + SEASON_YEAR  +"/players.json"
player_data = requests.get(player_url).json()

#ScheduleStuff
sched = Scheduler()
sched.start()

def update():
    global player_data
    player_data = requests.get(player_url).json()

sched.add_interval_job(update, hours=6)

#Stats
#(makes,attempts,statname)
FG_STATS = ["fgm","fga","FG","tpm","tpa","3PT","ftm","fta","FT"]

#(stat,statname)
TEAM_STATS = ["assists","AST","totReb","REB","blocks","BLK","steals","STL","turnovers","TO"]
PLAYER_LIVESTATS = ["assists","AST","totReb","REB","blocks","BLK","steals","STL","turnovers","TO","plusMinus","+/-","pFouls","fouls","min","mins"]
PLAYER_STATS = ["ppg","ppg","apg","apg","rpg","rpg","bpg","bpg","spg","spg","fgp","FG%","tpp","3PT%","ftp","FT%"]

#STATS IDS
TEAM_STATS_ID = 0
PLAYER_STATS_ID = 1
PLAYER_LIVESTATS_ID = 2

#GAME_STATUS_IDS
GAME_STATUS_BEFORE  = 1
GAME_STATUS_STARTED = 2
GAME_STATUS_FINAL   = 3

#SET TIME ZONE
TIME_ZONE = pytz.timezone('US/Eastern')

#Scoreboard update hour
SCOREBOARD_UPDATE_HOUR = 11

#&quote
hinkie_quotes=["The goal is simple: A larger quiver. This quiver will give us more options immediately and more options over time.",
                 "Why do we watch basketball games front to back? Why not watch games back to front, or out of order?",
                 "This approach, like many that create value, isn't popular, particularly locally.",
                 "It's about the willingness to say three simple words : I don't know.",
                 "You have to be non-consensus and right.",
                 "Fear has been the dominant motivator of the actions of too many for too long.",
                 "Maintain the longest view in the room.",
                 "Progress isn't linear.",
                 "We talk a lot about the process, not the outcome.",
                 "A new scientific truth does not triumph by convincing its opponents and making them see the light, but rather because its opponents eventually die.",
                 "Violence at the rim.",
                 "Grit matters.",
                 "In this league, the long view picks at the lock of mediocrity.",
                 "Team building is about one thing - the players.",
                 "Value optionality",
                 "You don't get to the moon by climbing a tree.",
                 "A competitive league like the NBA necessitates a zig while our competitors comfortably zag.",
                 "Sometimes the optimal place for your light is hiding directly under a bushel.",
                 "It is critical to be cycle aware in a talent-driven league."]

#BUNCH OF NAME SHIT
#Mapping IDs to names
id_to_team_name = {
    1610612737 : 'Hawks',
    1610612738 : 'Celtics',
    1610612751 : 'Nets',
    1610612766 :'Hornets',
    1610612741 : 'Bulls',
    1610612739 : 'Cavaliers',
    1610612742 : 'Mavericks',
    1610612743 : 'Nuggets',
    1610612765 : 'Pistons',
    1610612744 : 'Warriors',
    1610612745 : 'Rockets',
    1610612754 : 'Pacers',
    1610612746 : 'Clippers',
    1610612747 : 'Lakers',
    1610612763 : 'Grizzlies',
    1610612748 : 'Heat',
    1610612749 : 'Bucks',
    1610612750 : 'Timberwolves',
    1610612740 : 'Pelicans',
    1610612752 : 'Knicks',
    1610612760 : 'Thunder',
    1610612753 : 'Magic',
    1610612755 : 'Sixers',
    1610612756 : 'Suns',
    1610612757 :'Blazers',
    1610612758 : 'Kings',
    1610612759 :'Spurs',
    1610612761 : 'Raptors',
    1610612762 : 'Jazz',
    1610612764 : 'Wizards'
}


#Mapping teamID to conference
id_to_team_conf =  {
    1610612737 : 'east',
    1610612738 : 'east',
    1610612751 : 'east',
    1610612766 :'east',
    1610612741 : 'east',
    1610612739 : 'east',
    1610612742 : 'west',
    1610612743 : 'west',
    1610612765 : 'east',
    1610612744 : 'west',
    1610612745 : 'west',
    1610612754 : 'east',
    1610612746 : 'west',
    1610612747 : 'west',
    1610612763 : 'west',
    1610612748 : 'east',
    1610612749 : 'east',
    1610612750 : 'west',
    1610612740 : 'west',
    1610612752 : 'east',
    1610612760 : 'west',
    1610612753 : 'east',
    1610612755 : 'east',
    1610612756 : 'west',
    1610612757 :'west',
    1610612758 : 'west',
    1610612759 :'west',
    1610612761 : 'east',
    1610612762 : 'west',
    1610612764 : 'east'
}

#GAME_STATUS_IDS
GAME_STATUS_BEFORE  = 1
GAME_STATUS_STARTED = 2
GAME_STATUS_FINAL   = 3

#SET TIME ZONE
TIME_ZONE = pytz.timezone('US/Eastern')

#Scoreboard update hour
SCOREBOARD_UPDATE_HOUR = 11

#DIVISION CONFERENCES
WEST_CONF = ["southwest","pacific","northwest"]
EAST_CONF = ["southeast","atlantic","central"]

#conf names
conf_names = {
    "west" : "west",
    "western" : "west",
    "w" : "west",
    "western conference" : "west",
    "east" : "east",
    "eastern" : "east",
    "e" : "east",
    "pacific" : "pacific",
    "northwest": "northwest",
    "southwest": "southwest",
    "atlantic" : "atlantic",
    "central": "central",
    "southeast": "southeast",
    "tank" : "tank",
    "tankathon" : "tank"
}

#team name
teams_names = {
    'hawks': '1610612737',
    'atlanta': '1610612737',
    'atl': '1610612737',
    'atlanta hawks': '1610612737',
    'celtics': '1610612738',
    'boston': '1610612738',
    'bos': '1610612738',
    'boston celtics': '1610612738',
    'nets': '1610612751',
    'brooklyn': '1610612751',
    'brk': '1610612751',
    'brooklyn nets': '1610612751',
    'hornets': '1610612766',
    'charlotte': '1610612766',
    'cha': '1610612766',
    'charlotte hornets': '1610612766',
    'bulls': '1610612741',
    'chicago': '1610612741',
    'chi': '1610612741',
    'chicago bulls': '1610612741',
    'cavaliers': '1610612739',
    'cleveland': '1610612739',
    'cle': '1610612739',
    'cleveland cavaliers': '1610612739',
    'cavs': '1610612739',
    'mavericks': '1610612742',
    'dallas': '1610612742',
    'dal': '1610612742',
    'dallas mavericks': '1610612742',
    'mavs': '1610612742',
    'nuggets': '1610612743',
    'denver': '1610612743',
    'den': '1610612743',
    'denver nuggets': '1610612743',
    'pistons': '1610612765',
    'detroit': '1610612765',
    'det': '1610612765',
    'detroit pistons': '1610612765',
    'warriors': '1610612744',
    'golden state': '1610612744',
    'gsw': '1610612744',
    'golden state warriors': '1610612744',
    'rockets': '1610612745',
    'houston': '1610612745',
    'hou': '1610612745',
    'houston rockets': '1610612745',
    'pacers': '1610612754',
    'indiana': '1610612754',
    'ind': '1610612754',
    'indiana pacers': '1610612754',
    'clippers': '1610612746',
    'la clippers': '1610612746',
    'lac': '1610612746',
    'los angeles clippers': '1610612746',
    'lakers': '1610612747',
    'la lakers': '1610612747',
    'lal': '1610612747',
    'los angeles lakers': '1610612747',
    'grizzlies': '1610612763',
    'memphis': '1610612763',
    'mem': '1610612763',
    'memphis grizzlies': '1610612763',
    'heat': '1610612748',
    'miami': '1610612748',
    'mia': '1610612748',
    'miami heat': '1610612748',
    'bucks': '1610612749',
    'milwaukee': '1610612749',
    'mil': '1610612749',
    'milwaukee bucks': '1610612749',
    'timberwolves': '1610612750',
    'minnesota': '1610612750',
    'min': '1610612750',
    'wolves': '1610612750',
    'twolves' : '1610612750',
    'minnesota timberwolves': '1610612750',
    'pelicans': '1610612740',
    'new orleans': '1610612740',
    'nop': '1610612740',
    'pels': '1610612740',
    'new orleans pelicans': '1610612740',
    'knicks': '1610612752',
    'new york': '1610612752',
    'nyk': '1610612752',
    'new york knicks': '1610612752',
    'thunder': '1610612760',
    'oklahoma city': '1610612760',
    'okc': '1610612760',
    'oklahoma city thunder': '1610612760',
    'magic': '1610612753',
    'orlando': '1610612753',
    'orl': '1610612753',
    'orlando magic': '1610612753',
    'sixers': '1610612755',
    'philadelphia': '1610612755',
    '76ers': '1610612755',
    '6ers': '1610612755',
    'phi': '1610612755',
    'philadelphia 76ers': '1610612755',
    'suns': '1610612756',
    'phoenix': '1610612756',
    'phx': '1610612756',
    'phoenix suns': '1610612756',
    'blazers': '1610612757',
    'portland': '1610612757',
    'por': '1610612757',
    'trail blazers': '1610612757',
    'portland trail blazers': '1610612757',
    'kings': '1610612758',
    'sacramento': '1610612758',
    'sac': '1610612758',
    'sacramento kings': '1610612758',
    'spurs': '1610612759',
    'san antonio': '1610612759',
    'sas': '1610612759',
    'san antonio spurs': '1610612759',
    'raps': '1610612761',
    'raptors': '1610612761',
    'toronto': '1610612761',
    'craps': '1610612761',
    'tor': '1610612761',
    'toronto raptors': '1610612761',
    'jazz': '1610612762',
    'utah': '1610612762',
    'uta': '1610612762',
    'utah jazz': '1610612762',
    'wizards': '1610612764',
    'washington': '1610612764',
    'wsh': '1610612764',
    'wiz' : '1610612764',
    'washington wizards': '1610612764'
}


