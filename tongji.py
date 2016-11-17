#coding=utf-8
from peewee import *
import conf
import db0_conn as db0,db_conn1 as db1,db_conn2 as db2,time,redis

r=redis.Redis(host='192.168.230.128',port=6379,db=0)

def get_chk_time():
    """获得当天0点时间戳"""
    now = time.time()
    midnight = (now - (now % 86400) + time.timezone)*1000
    return midnight


def waiting_time(midnight):
    """定时更新等待时间，更新当天和历史最大更新时间"""
    query_today = db0.TaskidWorker.select(db0.TaskidWorker.add_time,db0.TaskidWorker.updatetime).where(db0.TaskidWorker.updatetime >= midnight)
    ret= db0.database.execute(query_today)
    for i in ret:
        waiting_time = i[1]-i[0]
        waiting_time_max_today = r.get("waiting_time_max_today")
        waiting_time_max_history = r.get("waiting_time_max_history")
        q = max(waiting_time,waiting_time_max_today)
        p = max(waiting_time,waiting_time_max_history)
        r.set("waiting_time_max_today",q)
        r.set("waiting_time_max_history",p)

def sus(midnight):
    """获得当日成功任务"""
    sus_today1 = db1.File.select().join(db1.TaskidFile).where((db1.File.status=="100000") & (db1.File.add_time > midnight)).count()
    sus_today2 = db2.File.select().join(db2.TaskidFile).where((db2.File.status=="100000") & (db2.File.add_time > midnight)).count()
    sus_today = sus_today1 + sus_today2
    r.set("sus_today",sus_today)
    sus_history1 = db1.File.select().join(db1.TaskidFile).where(db1.File.status=="100000").count()
    sus_history2 = db2.File.select().join(db2.TaskidFile).where(db2.File.status == "100000").count()

    sus_history = sus_history1 + sus_history2
    r.set("sus_history",sus_history)

def shibai(midnight):
    """获得当日失败任务"""
    sus_today1 = db1.File.select().join(db1.TaskidFile).where((db1.File.status=="1")&(db1.File.add_time > midnight)).count()
    sus_today2 = db2.File.select().join(db2.TaskidFile).where((db2.File.status=="1")&(db2.File.add_time > midnight)).count()
    sus_today = sus_today1 + sus_today2
    r.set("fail_today",sus_today)
    sus_history1 = db1.File.select().join(db1.TaskidFile).where(db1.File.status=="1").count()
    sus_history2 = db2.File.select().join(db2.TaskidFile).where(db2.File.status == "1").count()
    sus_history = sus_history1 + sus_history2
    r.set("fail_history",sus_history)

def consuming(midnight):
    """当日耗时分布计算"""
    cha = []
    less1 = 0
    One_to_Five = 0
    Five_to_Thirty = 0
    MoreThirty = 0
    query = db1.File.select(db1.File.add_time,db1.File.finishedtime).join(db1.TaskidFile).where((db1.File.status == "100000") & (db1.File.updatetime >= midnight))
    ret = db1.database.execute(query)
    for i in  ret:
        m = i[1] - i[0]
        cha.append(m)
    query = db2.File.select(db2.File.add_time,db2.File.finishedtime).join(db2.TaskidFile).where((db2.File.status == "100000") & (db2.File.updatetime >= midnight))
    ret = db2.database.execute(query)
    for i in  ret:
        m = i[1] - i[0]
        cha.append(m)

    for i in cha:
        if i <= 60000:
            less1 += 1
        elif(i>60000)&(i<=300000):
            One_to_Five += 1
        elif(i>300000)&(i<=1800000):
            Five_to_Thirty += 1
        else:
            MoreThirty += 1
    r.set("less1_today", less1)
    r.set("One_to_Five_today", One_to_Five)
    r.set("Five_to_Thirty_today", Five_to_Thirty)
    r.set("MoreThirty_today", MoreThirty)


def consuming_history():
    """历史耗时计算"""
    cha = []
    less1 = 0
    One_to_Five = 0
    Five_to_Thirty = 0
    MoreThirty = 0
    query = db1.File.select(db1.File.add_time, db1.File.finishedtime).join(db1.TaskidFile).where(
        db1.File.status == "100000")
    ret = db1.database.execute(query)
    for i in ret:
        m = i[1] - i[0]
        cha.append(m)
    query = db2.File.select(db2.File.add_time, db2.File.finishedtime).join(db2.TaskidFile).where(
        db2.File.status == "100000")
    ret = db2.database.execute(query)
    for i in ret:
        m = i[1] - i[0]
        cha.append(m)
    for i in cha:
        if i < 60000:
            less1 += 1
        elif (i > 60000 and i <= 300000):
            One_to_Five += 1
        elif (i > 300000 and i <= 1800000):
            Five_to_Thirty += 1
        else:
            MoreThirty += 1
    r.set("less1_history", less1)
    r.set("One_to_Five_history", One_to_Five)
    r.set("Five_to_Thirty_history", Five_to_Thirty)
    r.set("MoreThirty_history", MoreThirty)

def downloading(midnight):
    """下载时间统计"""
    count = 0
    query = db1.TaskidFile.select(db1.TaskidFile.add_time,db1.TaskidFile.update_time).where(db1.TaskidFile.update_time != "-1")
    cur = db1.database.execute(query)
    for i in cur:
        download_time = i[1] - i[0]
        if download_time>conf.threshold:
            count += 1
    query = db2.TaskidFile.select(db2.TaskidFile.add_time,db2.TaskidFile.update_time).where(db2.TaskidFile.update_time != "-1")
    cur = db2.database.execute(query)
    for i in cur:
        download_time = i[1] - i[0]
        if download_time>conf.threshold:
            count += 1
    r.set('download_time_count_history',count)

    count = 0
    query = db1.TaskidFile.select(db1.TaskidFile.add_time,db1.TaskidFile.update_time).where((db1.TaskidFile.update_time != "-1")&(db1.TaskidFile.add_time > midnight))
    cur = db1.database.execute(query)
    for i in cur:
        download_time = i[1] - i[0]
        if download_time>conf.threshold:
            count += 1
    query = db2.TaskidFile.select(db2.TaskidFile.add_time,db2.TaskidFile.update_time).where((db2.TaskidFile.update_time != "-1")&(db2.TaskidFile.add_time > midnight))
    cur = db2.database.execute(query)
    for i in cur:
        download_time = i[1] - i[0]
        if download_time>conf.threshold:
            count += 1
    r.set('download_time_count_today',count)


def Day7_task(midnight):

    Day_time_midnight = []
    for i in range(8):
        mid = midnight - 86400000*i
        Day_time_midnight.append(mid)

        # 7天内每天接到的任务
    Day_count = []
    for i in range(7):
        q1 = db0.TaskidWorker.select().where((db0.TaskidWorker.add_time < Day_time_midnight[i])&(db0.TaskidWorker.add_time > Day_time_midnight[i+1] )).count()
        Day_count.append(q1)
    for i in range(7):
        key1 = "task_day_before" + str(i)
        r.set(key1,Day_count[i])

#   7天内每天领取的任务
    Task_count = []
    for i in range(7):
        q2 = db0.TaskidWorker.select().where((db0.TaskidWorker.updatetime < Day_time_midnight[i])&(db0.TaskidWorker.updatetime > Day_time_midnight[i+1] )).count()
        Day_count.append(q2)
    for i in range(7):
        key2 = "deal_day_before" + str(i)
        r.set(key2,Day_count[i])



if __name__ == "__main__":
    midnight = get_chk_time()
    waiting_time(midnight)
    sus(midnight)
    shibai(midnight)
    consuming(midnight)
    consuming_history()
    downloading(midnight)
    Day7_task(midnight)








