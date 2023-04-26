import pymqi
import os
import xml
import re

#UAT
queue_manager = "QMNAME"
channel = "SVRCONN.NAME"
host = "qm.example.com"
port = "1417"
queue_name = "queue_name.inp"
user = 'example_user@DOMAIN'
password = None

conn_info = '%s(%s)' % (host, port)
qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password='' )

queue_backout = pymqi.Queue(qmgr, queue_name)

# Message Descriptor
md = pymqi.MD()

# Get Message Options
gmo = pymqi.GMO()
gmo.Options = pymqi.CMQC.MQGMO_WAIT | pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING
gmo.WaitInterval = 500000 # 5 seconds

while True:
    message = queue_backout.get_no_rfh2(None, md, gmo)
    #os.sleep(1000000000000)
    print(message)

queue_backout.close()
queue.close()

qmgr.disconnect()