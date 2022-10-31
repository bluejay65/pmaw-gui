from pmaw import PushshiftAPI
import datetime
import time as t
import os

seconds_per_day = 3600*24
seconds_per_month = seconds_per_day*30
seconds_per_year = seconds_per_month * 12 + 5 * seconds_per_day

months_saved = 0
years_saved = 0

api = PushshiftAPI(shards_down_behavior=None)

comment_dict = {}
month_dict = {}
year_dict = {}

def epoch_to_date(epoch):
    return datetime.date.fromtimestamp(epoch)

def save_file(dict):
    file_name = str(list(dict.keys())[0])+' - '+str(list(dict.keys())[-1])
    file = os.path.join(os.path.join(os.getcwd(), 'missing comment data'), file_name+".csv")
    with open(file, 'w') as f:
        f.write('Date,Presence\n')
        for i in dict.keys():
            f.write(str(i)+','+dict[i]+'\n')

def date_time_to_epoch(date: datetime.date, time: datetime.time):
    struct_time = t.struct_time([date.year, date.month, date.day, time.hour, time.minute, 0, 0, 1, -1])
    return int(t.mktime(struct_time))

start_date = date_time_to_epoch(datetime.date(2019, 9, 11), datetime.time(0, 0))
date_offset = start_date % seconds_per_day

for day in range(start_date,
    date_time_to_epoch(datetime.date.today(), datetime.time(0, 0)),
    seconds_per_day):
    t.sleep(5)

    comments = api.search_comments(limit=10, q='e', after=day, before=day+seconds_per_day)
    if len(comments) > 0:
        month_dict[epoch_to_date(day)] = 'Available'
        print('Available: '+str(epoch_to_date(day)))
    else:
        month_dict[epoch_to_date(day)] = "Missing"
        print('MISSING: '+str(epoch_to_date(day)))

    if day % seconds_per_month - date_offset == 0:
        save_file(month_dict)
        months_saved = months_saved + 1
        year_dict.update(month_dict)
        month_dict = {}

    if day % seconds_per_year - date_offset == 0:
        years_saved = years_saved + 1
        year_dict.update(month_dict)
        comment_dict.update(year_dict)
        save_file(year_dict)
        year_dict = {}


save_file(comment_dict)