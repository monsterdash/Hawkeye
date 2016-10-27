from flask import Flask,render_template
from flask.views import  View
import db_conn as db

app = Flask(__name__)


class COMMON(View):
    def __init__(self):
        self.data = []


    def dispatch_request(self):

        db.database.connect()
        query =  db.File.select(db.TaskidFile.file,db.File.id,db.File.status) \
                .join(db.TaskidFile) \
                .order_by(db.File.id)
        self.data = db.database.execute(query)

        return render_template('index.html', data=self.data)



app.add_url_rule('/', view_func=COMMON.as_view('index'))






if __name__ == '__main__':
    app.secret_key = 'whoisyourdaddy'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='127.0.0.1',debug='true')