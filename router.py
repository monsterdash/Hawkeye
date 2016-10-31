import db_conn1,db_conn2,db0_conn

def link_db(condition):
    db_ip = db0.Taskid_worker.select(db0.Worker.ip).join(db0.Worker).where(db0.Taskid_worker.task_id == condition)
    if db_ip =="":
        db_conn1.database1.connect()
    else:
        db_conn2.database2.connect()
    return  db_ip

