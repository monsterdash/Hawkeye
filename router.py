import db_conn1,db_conn2,db0_conn as db0
import conf


def router(condition):
        db_ip = db0.TaskidWorker.select(db0.Worker.ip).join(db0.Worker).where(db0.TaskidWorker.task == condition)
        ret = db0.database.execute(db_ip)
        db = db_conn1
        for i in ret:
            sea = i[0]
            if sea  == "MTkyLjE2OC4xMC4xMjc=":
                db = db_conn1
            else:
                db = db_conn2
        return db


class resolve():
    def __init__(self,db,condition,order,page,desc):
        self.db = db
        self.qbase = db.File.select(db.TaskidFile.file, db.File.id, db.File.status).join(db.TaskidFile)
        self.cbase = db.File.select().join(db.TaskidFile)
        self.condition = condition
        # self.con_value = con_value
        self.order = order
        self.page = page
        self.desc = desc
        self.count = ''
        self.ret = ""
        element = {'id': db.File.id, 'md5': db.File.md5, 'sha256': db.File.sha256, 'status': db.File.status,
                   'task_id':db.TaskidFile.task }

        # def select_condition():
        #         for i in range(0, len(self.condition)):
        #             tj = element[condition[i]]
        #             zh = con_value[i]
        #             self.qbase = self.qbase.where(tj == zh)
        #             self.cbase = self.qbase.where(tj == zh)

    def select_condition(self):
        self.qbase = self.qbase.where(self.db.TaskidFile.id)
        self.cbase = self.cbase.where(self.db.TaskidFile.id)


    def take_order(self):
        element={}
        tj = element[self.order]
        if self.desc == True:
            self.qbase = self.qbase.order_by(tj,self.desc())
        else:
            self.qbase = self.qbase.order_by(tj)

    def take_page(self):
        self.qbase = self.qbase.paginate(self.page,conf.ROW_NUM)


    def parsing(self):
        if self.condition != []:
            self.select_condition()
        else:
            pass
        if self.order != '':
            self.take_order()
        else:
            self.qbase = self.qbase.order_by(self.db.File.id)
        self.take_page()
        self.count = self.cbase.count()