import time
#(tm_year=2021, tm_mon=8, tm_mday=24, tm_hour=9, tm_min=26, tm_sec=0, tm_wday=0, tm_yday=0, tmisdst=-1)
t = time.mktime((2021, 8, 24, 9, 6, 0, 0, 0, -1))
print(type(t), t)
print("Struct", time.localtime(t))
print("Struct2", time.struct_time((2021, 8, 24, 9, 6, 0, 0, 0, -1)))


result = time.localtime()
print("Local", result)