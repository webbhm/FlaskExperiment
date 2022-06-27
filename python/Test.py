byte = 0x88
print( hex(byte))
barray = [int(i) for i in "{0:08b}".format(byte)]
print( barray)

from datetime import datetime
ts = datetime.utcnow().isoformat()
print( ts)
print( len(ts))
print( ts[:19])

print("\nInvalid string format test")
temp = None
try:
    temp_s = "{:0.2f}".format(temp)
except Exception as e:
    print(e)
    
print("\nTest Env Object")
from env2 import env
print(getattr(env, 'foo'))
setattr(env, 'foo1', 2)
print(getattr(env, 'foo1'))
print(getattr(env, 'foo2'))