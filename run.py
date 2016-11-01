from flask import Flask,render_template,request
from flask.views import  View
import conf,router
import resolver
import db0_conn as db0

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
            if form.haskey(i):
                pass
            else:
                return "error"
        db = router.switch_db(form['condition'])
        dx = resolver.resolve(form['codition'],form['order'],form['page'],form['desc'])
        dx.parsing
        query = dx.qbase
        ret = db.database.execute(query)
        rows = dx.count
        data = []
        for i in ret:
            # 翻译status，字典在conf中
            sta0 = i[2]
            stat = conf.stadic[sta0]
            data.append({"Task_id":i[0],"File_id":i[1],"Status":stat})
        response = {"data":data,"row_num":rows}
        return response

@app.route('/error_msg/<task_id>')
def error_msg(task_id):
    db = router.switch_db(task_id)
    query = db.ErrorMessage.select(db.ErrorMessage.crash_flag,db.ErrorMessage.error_message,db.ErrorMessage.error_location,db.ErrorMessage.error_type ) \
            .where(db.ErrorMessage.file == task_id)
    ret = db.database.execute(query)
    response=[]
    for i in ret:
        response.append(i)
    return render_template('error_msg.html',data = response)


if __name__ == '__main__':
    app.secret_key = 'whosyourdaddyandgreedyisgood'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='127.0.0.1',debug='true')