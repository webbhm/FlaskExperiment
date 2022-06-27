from datetime import datetime, timedelta


print datetime.utcnow()
#print datetime.utcfromtimestamp(datetime.now())

d=datetime.strptime('2018-11-08T10:30:20', '%Y-%m-%dT%H:%M:%S')
print d
epoch = datetime(1970,1,1,0,0,0, tzinfo=None)
print timedelta.total_seconds(d - epoch)
