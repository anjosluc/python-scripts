import pymqi
import os
import xml
import re

#PROD
queue_manager = "QMNAME"
channel = "CHANNELNAME"
host = "qm.example.com"
port = "1416"
queue_name = "queue.inp"

conn_info = '%s(%s)' % (host, port)

qmgr = pymqi.connect(queue_manager, channel, conn_info)
queue = pymqi.Queue(qmgr, queue_name)
regex = r"<\?xml.*<\/Line>"

with open("file.xml","r",encoding = "utf8" ) as file:
    data = file.readlines()
    for line in data:
        if re.match(regex, line):
            message = line.strip()
            print("MESSAGE IS:\n {}".format(line))
            queue.put(message)
            print("MESSAGE POSTED")

queue.close()
qmgr.disconnect()