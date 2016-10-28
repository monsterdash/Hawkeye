from flask import Flask,render_template,request
from flask.views import  View,MethodView
import query

import db_conn as db

app = Flask(__name__)

class Index(View):
    def __init__(self):
         self.data = []

    def dispatch_request(self):

        db.database.connect()
        query =  db.File.select(db.TaskidFile.file,db.File.id,db.File.status) \
                 .join(db.TaskidFile) \
               .order_by(db.File.id) \
                .limit(20)

        self.data = db.database.execute(query)
        return render_template('index.html', data=self.data)


app.add_url_rule('/', view_func=Index.as_view('index'))


@app.route('/select/',method=['GET'])
def select():
    if request.method == 'GET':
        args=['condition','con_value','order','page','desc']
        form = request.values.to_dict()
        for i in args:
            if form.haskey(i):
                pass
            else:
                return "error"
        dx = select.resolve(form['codition'],form['con_value'],form['order'],form['page'],form['desc'])
        query = dx.parse
        data = db.database.execute(query)
        return data










if __name__ == '__main__':
    app.secret_key = 'whosyourdaddyandgreedyisgood'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='127.0.0.1',debug='true')