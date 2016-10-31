import  db_conn as db
import conf

class resolve():
    def __init__(self,condition,con_value,order,page,desc):
        self.qbase = db.File.select(db.TaskidFile.file, db.File.id, db.File.status).join(db.TaskidFile)
        self.cbase = db.File.select().join(db.TaskidFile)
        self.condition = condition
        self.con_value = con_value
        self.order = order
        self.page = page
        self.desc = desc
        self.count = ''
        element = {'id': db.File.id, 'md5': db.File.md5, 'sha256': db.File.sha256, 'status': db.File.status,
                   'task_id':db.TaskidFile.task }

        def select_condition():
                for i in range(0, len(self.condition)):
                    tj = element[condition[i]]
                    zh = con_value[i]
                    self.qbase = self.qbase.where(tj == zh)
                    self.cbase = self.qbase.where(tj == zh)


        def take_order():
            tj = element[self.order]
            if self.desc == True:
                self.qbase = self.qbase.order_by(tj,desc())
            else:
                self.qbase = self.qbase.order_by(tj)

        def take_page():
            self.qbase = self.qbase.paginate(self.page,conf.ROW_NUM)


        def parsing():
            if self.condition != []:
                select_condition()
            else:
                pass
            if self.order != '':
                take_order()
            else:
                self.qbase = self.qbase.order_by(db.File.id)
            take_page()
            self.count = self.cbase.count()















