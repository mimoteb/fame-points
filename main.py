import requests, configparser, json, os, math, sqlite3
from datetime import datetime
from logger import log
con = sqlite3.connect('db.db')
con.row_factory = sqlite3.Row
dir = os.path.dirname(__file__)
config_file = os.path.join(dir, 'fame_points_config.ini')

config = configparser.ConfigParser()
config.read(config_file)

app_id = config.get('api', 'app_id')
realm = config.get('api', 'realm')
account_id = 542250529
front_id = 'thunderstorm_bg'
event_id = 'thunderstorm'
clan_id = '500063884'
now = datetime.now()
now = now.strftime('%d.%m.%Y')

def get_rank_cut(rank: int):
    page_no = math.ceil(rank/10)
    url = 'https://api.worldoftanks.eu/wot/globalmap/eventaccountratings/?application_id={}&front_id={}&event_id={}&page_no={}&limit=10&in_rating=1'.format(app_id,front_id, event_id,page_no)
    res = requests.post(url)
    res = json.loads(res.text)
    for r in res['data']:
        if r['rank']==rank:
            return(r['fame_points'])

cutoff = get_rank_cut(8000)
style_rank = get_rank_cut(4000)

def update_points_cut():
    if cutoff is not None:
        cur = con.cursor()
        query = "update exp set req = '{}' where day = '{}'".format(cutoff, now)
        cur.execute(query)
        con.commit()

def update_diff_grow():
    cur = con.cursor()
    query = "select * from exp where front ='{}' and req > 0".format(front_id)
    cur.execute(query)
    result = cur.fetchall()
    count = len(result)
    today = None
    for i in range(count):
        if today is not None and result[i]['req'] > 0:
            day = result[i]['day']
            yesterday_cutoff = int(result[i-1]['req'])
            today_cutoff = int(result[i]['req'])
            diff = today_cutoff - yesterday_cutoff
            diff_yesterday = result[i-1]['diff']
            grow = round(diff / diff_yesterday,3)
            query = "update exp set diff='{}', grow='{}' where day='{}'".format(diff, grow, day)
            cur.execute(query)
            con.commit()
        today = result[i]
def expect():
    cur = con.cursor()
    query = "select * from exp where req <> 0 and front='{}'".format(front_id)
    cur.execute(query)
    result = cur.fetchall()
    total_avg = 0
    avg = 0
    for i in range(len(result)):
        total_avg +=result[i]['avg']
    avg = round(total_avg / len(result), 3)

    query = "update exp set avg='{}' where front='{}' and req<>0".format(avg, front_id)
    cur.execute(query)
    con.commit()

def calc():
    cur = con.cursor()
    query = "select * from exp where front ='{}'".format(front_id)
    cur.execute(query)
    result = cur.fetchall()
    last_cut = 0
    avg_grow = 1.28
    last_diff = 0
    for i in range(len(result)):
        if result[i]['diff'] > 0:
            last_diff = result[i]['diff']
        
        if result[i]['req'] > 0:
            last_cut = result[i]['req']
        
        day = result[i]['day']
        day_num = result[i]['day_num']
        req = int(result[i]['req'])
        if result[i]['req'] > 0:
            print('day: {} ({}) Points cut: {}'.format(day_num, day, req))
        else:
            expected_cut = (avg_grow * last_diff) + last_cut
            last_diff = avg_grow * last_diff
            last_cut = expected_cut
            print('day: {} ({}) expected points: {}'.format(day_num, day, int(expected_cut)))

update_points_cut()
update_diff_grow()
calc()
print('Cutoff Now: {}'.format(cutoff))
print('Top 4k Now: {}'.format(style_rank))
log('cut off: {}'.format(cutoff))
log('top 4k: {}'.format(style_rank))
con.close()