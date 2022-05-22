import configparser
from datetime import datetime
import os
dir = os.path.dirname(__file__)
config = configparser.ConfigParser()
config_file = os.path.join(dir, 'fame_points_config.ini')
config.read(config_file)
app_id = config.get('api', 'app_id')
realm = config.get('api', 'realm')
account_id = 542250529
front_id = 'thunderstorm_bg'
event_id = 'thunderstorm'
log_file_name = 'players_list.txt'

dir = os.path.dirname(__file__)
log_file = os.path.join(dir, log_file_name)

def log(content: str):
    try:
        file = open(log_file,'w')
        file.write(content + '\n')
        file.close()
    except Exception as e:
        print(str(e))
def print_players():
    print(datetime.now().strftime('%d.%m.%Y - %H:%M'))

print_players()