import os
from datetime import datetime

log_file_name = 'fame_points_log.txt'
dir = os.path.dirname(__file__)
log_file = os.path.join(dir, log_file_name)

def log(content: str):
    log_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    try:
        file = open(log_file,'a')
        file.write(log_time + ' - ' + content + '\n')
        file.close()
    except Exception as e:
        print(str(e))