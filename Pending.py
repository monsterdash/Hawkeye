
import db0_conn as db0,db_conn1 as db1,db_conn2 as db2
import base64,operator,time

def pending_item():
    items=[]
    query = db0.TaskidWorker.select(db0.TaskidWorker.task,db0.TaskidWorker.add_time,db0.TaskidWorker.scan_app_url).where(db0.TaskidWorker.updatetime == "-1")
    waiting_item = db0.database.execute(query)
    for i in waiting_item:
        url64 = base64_dec(i[2])
        ctime = time_change(i[1])
        items.append({"Task_id":i[0],"add_time":ctime,"scan_app_url":url64})
    return items

def done_task():
    data = []
    query1 = db1.File.select(db1.TaskidFile.task,db1.TaskidFile.add_time,db1.TaskidFile.scan_app_url).join(db1.TaskidFile).where(db1.File.status == "100000")
    query2 = db2.File.select(db2.TaskidFile.task,db2.TaskidFile.add_time,db2.TaskidFile.scan_app_url).join(db2.TaskidFile).where(db2.File.status == "100000")
    ret1 = db1.database.execute(query1)
    ret2 = db2.database.execute(query2)
    for i in ret1:
        url64 = base64_dec(i[2])
        ctime = time_change(i[1])
        data.append({"task_id":i[0],"add_time":ctime,"scan_app_url":url64})
    for i in ret2:
        url64 = base64_dec(i[2])
        ctime = time_change(i[1])
        data.append({"task_id":i[0],"add_time":ctime,"scan_app_url":url64})
    data = sorted(data, key=operator.itemgetter('add_time'),reverse = True)
    return data

def base64_dec(st):
    p1 = base64.b64decode(st)
    p2 = base64.b64decode(p1)
    p3 = p2.decode('utf8')
    return p3

def time_change(ti):
    itime1000 = int(ti)
    itime = int(itime1000/1000)
    ltime = time.localtime(itime)
    ctime = time.strftime("%Y-%m-%d %H:%M:%S", ltime)
    return ctime