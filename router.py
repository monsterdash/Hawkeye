import db_conn1,db_conn2,db0_conn as db0

def switch_db(condition):
    db_conn1.database1.connect()
    db_conn2.database2.connect()
    db_ip = db0.Taskid_worker.select(db0.Worker.ip).join(db0.Worker).where(db0.Taskid_worker.task_id == condition)
    if db_ip =="":
        db_conn = db_conn1
    else:
        db_conn = db_conn2
    return  db_conn

