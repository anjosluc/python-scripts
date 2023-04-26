import pymqi
import os
import xml
import re

#PROD
queue_manager = "QMNAME"
channel = "CHANNEL"
host = "qm.example.com"
port = "1416"
conn_info = '%s(%s)' % (host, port)
qmgr = pymqi.connect(queue_manager, channel, conn_info)

queue_backout = pymqi.Queue(qmgr, "queue.bck")
queue = pymqi.Queue(qmgr, "queue.inp")

while True:
    message = queue_backout.get_no_rfh2()
    #print(message)
    queue.put(str(message))
    print("MESSAGE POSTED:\n {}".format(str(message)))

queue_backout.close()
queue.close()

qmgr.disconnect()