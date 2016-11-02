#coding=utf-8
from flask import Flask,render_template,request,jsonify
from flask.views import  View
import conf,router

app = Flask(__name__)

class Index(View):
    def __init__(self):
         self.data = {}

    def dispatch_request(self):
        # data0 = []
        # db1.database.connect()
        # query =  db1.File.select(db1.TaskidFile.file,db1.File.id,db1.File.status) \
        #          .join(db1.TaskidFile) \
        #        .order_by(db1.File.id) \
        #         .limit(20)
        # ret = db1.database.execute(query)
        #
        # for i in ret:
        #     sta0 = i[2]
        #     stat = conf.stadic[sta0]
        #     data0.append({"Task_id": i[0], "File_id": i[1], "Status": stat})
        # rows = db1.File.select().join(db1.TaskidFile).count()
        # self.data = {"data":data0,"row_num":rows}
        # db1.database.close()
        return render_template('index.html', response=self.data)


app.add_url_rule('/', view_func=Index.as_view('index'))


@app.route('/select/',methods=['GET'])
def select():
    if request.method == 'GET':
        args=['condition','order','page','desc']
        form = request.values.to_dict()
        for i in args:
            if i in form:
                pass
            else:
                form[i] = ""
        dy = router.router(form['condition'])
        dx = router.resolve(dy,form['condition'],form['order'],form['page'],form['desc'])
        dx.parsing()
        q = dx.qbase
        ret = dy.database.execute(q)
        rows = 0
        data = []
        for i in ret:
            # 翻译status，字典在conf中
            sta0 = i[2]
            stat = conf.stadic[sta0]
            data.append({"Task_id":i[0],"File_id":i[1],"Status":stat})
            rows = rows +1
        det = {"data":data,"row_num":rows}
        return jsonify(det)


@app.route('/test')
def test():
    import db_conn1
    d=[]
    c = db_conn1.ErrorMessage.select().where(db_conn1.ErrorMessage.file == "1")
    for i in c:
        d.append(i)
    return d





@app.route('/error_msg',methods=['POST'])
def error_msg():
    if request.method == "POST":
        file_id = request.form["file_id"]
        task_id = request.form["task_id"]
        db = router.router(task_id)
        query = db.ErrorMessage.select(db.ErrorMessage.crash_flag, db.ErrorMessage.error_message,
                                       db.ErrorMessage.error_location, db.ErrorMessage.error_type) \
                                        .where(db.ErrorMessage.file == file_id)
        ret = db.database1.execute(query)
        res = {"data":[]}
        row_num = 0
        for i in ret:
            tm = {"crash_flag":i[0],"error_msg":i[1],"error_location":i[2],"error_type":i[3]}
            res['data'].append(tm)
            row_num = row_num + 1
        if row_num == 0:
            return "No error message"
        else:
            return render_template('error_msg.html', data=res)








if __name__ == '__main__':
    app.secret_key = 'whosyourdaddyandgreedyisgood'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='127.0.0.1',debug='true')