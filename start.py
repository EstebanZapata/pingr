import os
from pythonping import ping

target = os.environ.get('TARGET')
ping(target, count=1, verbose=True)
print('done')