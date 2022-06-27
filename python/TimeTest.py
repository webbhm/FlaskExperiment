from datetime import datetime
from datetime import timedelta

t = datetime.now()
t = t - timedelta(weeks=4)
print t
t = t + timedelta(days=1)
print t
t = t + timedelta(minutes=20)
print t
t = t.replace(hour=10, minute=30)
print t
timestamp = datetime.now()
tm = timestamp.strftime('%y/%m/%d %H:%M%S')
t2 = datetime.strptime(tm, '%y/%m/%d %H:%M%S')
print 'Time from String', t2
#t3 = datetime.strptime('2018-08-02 11:20:00', '%y-%m-%d')
print 'Time from String - 2', t3
#t3 = datetime.strptime('2018-08-02 11:20', '%y-%m-%d')
print 'Time from String - 2', t3
tt = datetime.now().timetuple()
print tt
t = datetime.now()
print "weeks", t.strftime("%W"), t.isocalendar()[1], t.strftime("%V")

def getDateStruct():
    t = datetime.now()
    timestamp = t.isoformat()
    parts = [t.strftime('%Y'), t.strftime('%m'), t.strftime('%d'), t.strftime('%H'), t.strftime('%M'), t.strftime('%S')]
    dt = {'timestamp':timestamp, 'parts': parts, 'week':t.strftime('%V')}
    return dt

print getDate()    


