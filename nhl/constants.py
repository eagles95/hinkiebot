import requests
from apscheduler.scheduler import Scheduler

#Current Season
CURRENT_SEASON = "20182019"


player_info_url = "http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=basic&isGame=false&reportName=skatersummary&sort=[{%22property%22:%22points%22,%22direction%22:%22DESC%22},{%22property%22:%22goals%22,%22direction%22:%22DESC%22},{%22property%22:%22assists%22,%22direction%22:%22DESC%22}]&cayenneExp=gameTypeId=2%20and%20seasonId%3E="+ CURRENT_SEASON +"%20and%20seasonId%3C=" + CURRENT_SEASON
goalie_info_url = "http://www.nhl.com/stats/rest/goalies?isAggregate=false&reportType=goalie_basic&isGame=false&reportName=goaliesummary&sort=[{%22property%22:%22wins%22,%22direction%22:%22DESC%22}]&cayenneExp=gameTypeId=2%20and%20seasonId%3E="+CURRENT_SEASON+"%20and%20seasonId%3C="+CURRENT_SEASON
player_data = requests.get(player_info_url).json()
goalie_data = requests.get(goalie_info_url).json()

#ScheduleStuff
sched = Scheduler()
sched.start()


def update():
    global player_data
    player_data = requests.get(player_info_url).json()
    global goalie_data
    goalie_data = requests.get(goalie_info_url).json()

sched.add_interval_job(update, hours=6)


#ID STUFF
team_name_to_id = {
 'devils': '01',
 'islanders': '02',
 'islies' : '02',
 'rangers': '03',
 'rags': '03',
 'flyers': '04',
 'phi': '04',
 'flyera': '04',
 'philadelphia': '04',
 'philadelphia flyers': '04',
 'pens': '05',
 'penguins': '05',
 'bruins': '06',
 'sabres': '07',
 'habs': '08',
 'canadiens': '08',
 'sens': '09',
 'senators': '09',
 'leafs': '10',
 'canes': '12',
 'hurricanes': '12',
 'panthers': '13',
 'bolts': '14',
 'lightning': '14',
 'caps': '15',
 'capitals': '15',
 'hawks': '16',
 'blackhawks': '16',
 'wings': '17',
 'red wings': '17',
 'preds': '18',
 'predators': '18',
 'blues': '19',
 'flames': '20',
 'avs': '21',
 'avalanche': '21',
 'oilers': '22',
 'canucks': '23',
 'ducks': '24',
 'stars': '25',
 'kings': '26',
 'yotes': '53',
 'coyotes': '53',
 'sharks': '28',
 'jackets': '29',
 'blue jackets': '29',
 'wild': '30',
 'jets': '52',
 'knights': '54'
}



