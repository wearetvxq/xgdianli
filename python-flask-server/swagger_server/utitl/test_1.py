import datetime
#测试提交

def ttt(StartDate='', EndDate=''):
    print(11)

    d1 = StartDate
    d2 = EndDate
    print('d1:',d1)
    print('d2:',d2)
    date1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
    date2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
    delta = date2 - date1
    print('delta:', delta)
    per_day_seconds = 24 * 60 * 60
    per_week_seconds = 7 * per_day_seconds
    total_seconds = delta.total_seconds()
    weeks = total_seconds // per_week_seconds
    days = total_seconds // per_day_seconds
    if weeks * per_week_seconds < total_seconds:
        weeks += 1

    oneday = datetime.timedelta(days=1)
    WEEK = ["M", "T", "W", "R", "F", "S", "U"]

    d0 = date1
    weekdays = [d0, ]
    weekday_all = []
    enday = datetime.datetime.strptime(d1, "%Y-%m-%d")
    for i in range(int(days)):
        weekday_part = []
        d0 += oneday
        if d0.weekday() == 6:  # For Sunday
            per_week = []
            for d in weekdays:
                per_week.append(d.strftime("%Y-%m-%d"))
                enday = d.strftime("%Y-%m-%d")
                enday = datetime.datetime.strptime(enday, "%Y-%m-%d")
            print('--per_week---', per_week)
            weekdays = []
        weekdays.append(d0)
    if enday != date2:
        per_week = []
        enday += datetime.timedelta(days=1)
        while enday <= date2:
            date_str = enday.strftime("%Y-%m-%d")
            per_week.append(date_str)
            enday += datetime.timedelta(days=1)
        print('--per_week---', per_week)

if __name__ == '__main__':
    print('comming')
    ttt('2017-07-11', '2017-09-18')
