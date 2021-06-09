import threading
import time

def worker(num):
    try:
        """thread worker function"""
        print ('S:%s ' % num, end="")
        time.sleep(10)
        print ('E:%s ' % num, end="")
        return
    except Exception:
        print ("Exception")
    

a = time.time()
threads = []
for i in range(10000):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
    
b = time.time()
print (">>>>>>" + str(b-a))

for t in threads:
    t.join()
    
c = time.time()
print ("=======================" + str(c-a))
