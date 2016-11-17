#coding=utf-8
from flask import Flask,render_template,request,jsonify
from flask.views import  View
import conf,router,redis_con,Pending

app = Flask(__name__)

class Index(View):

    def dispatch_request(self):
        data = {}
        data["waiting_time_max_today"] = int(redis_con.r.get("waiting_time_max_today"))
        data["waiting_time_max_history"] = int(redis_con.r.get("waiting_time_max_history"))
        data["sus_today"] =  int(redis_con.r.get("sus_today"))
        data["sus_history"] = int(redis_con.r.get("sus_history"))
        data["fail_today"] = int(redis_con.r.get("fail_today"))
        data["fail_history"] = int(redis_con.r.get("fail_history"))
        data["less1_today"] = int(redis_con.r.get("less1_today"))
        data["One_to_Five_today"] = int(redis_con.r.get("One_to_Five_today"))
        data["Five_to_Thirty_today"] = int(redis_con.r.get("Five_to_Thirty_today"))
        data["MoreThirty_today"] = int(redis_con.r.get("MoreThirty_today"))
        data["less1_history"] = int(redis_con.r.get("less1_history"))
        data["One_to_Five_history"] = int(redis_con.r.get("One_to_Five_history"))
        data["Five_to_Thirty_history"] = int(redis_con.r.get("Five_to_Thirty_history"))
        data["MoreThirty_history"] = int(redis_con.r.get("MoreThirty_history"))
        data["download_time_count_history"] = int(redis_con.r.get("download_time_count_history"))
        data["download_time_count_today"] = int(redis_con.r.get("download_time_count_today"))
        data["task_day_before0"] = int(redis_con.r.get("task_day_before0"))
        data["task_day_before1"] = int(redis_con.r.get("task_day_before1"))
        data["task_day_before2"] = int(redis_con.r.get("task_day_before2"))
        data["task_day_before3"] = int(redis_con.r.get("task_day_before3"))
        data["task_day_before4"] = int(redis_con.r.get("task_day_before4"))
        data["task_day_before5"] = int(redis_con.r.get("task_day_before5"))
        data["task_day_before6"] = int(redis_con.r.get("task_day_before6"))
        data["deal_day_before0"] = int(redis_con.r.get("deal_day_before0"))
        data["deal_day_before1"] = int(redis_con.r.get("deal_day_before1"))
        data["deal_day_before2"] = int(redis_con.r.get("deal_day_before2"))
        data["deal_day_before3"] = int(redis_con.r.get("deal_day_before3"))
        data["deal_day_before4"] = int(redis_con.r.get("deal_day_before4"))
        data["deal_day_before5"] = int(redis_con.r.get("deal_day_before5"))
        data["deal_day_before6"] = int(redis_con.r.get("deal_day_before6"))
        pendings = Pending.pending_item()
        done_task = Pending.done_task()
        working_task = Pending.working_task()
        error_task = Pending.error_task()
        return render_template('index.html',data = data,pendings = pendings,done_task=done_task,working_task = working_task,error_task = error_task)

app.add_url_rule('/', view_func=Index.as_view('index'))


@app.route('/select/',methods=['GET'])
def select():
    if request.method == 'GET':
        args=['condition','order','page','desc']
        form = request.values.to_dict()
        for i in args:
            form.setdefault(i, "")
        # 路由分库取得所在数据库dy ↓
        dy = router.router(form['condition'])
        # 生成对象dx ↓
        dx = router.resolve(dy, form['condition'],form['order'],form['page'],form['desc'])
        dx.parsing()
        q = dx.qbase
        count = dx.qbase.count()
        if count == 0:
            return jsonify(error_code = 'error')
        else:
        # q = dy.TaskidFile.select(dy.TaskidFile.task,dy.TaskidFile.file,dy.File.status).join(dy.File).where(dy.TaskidFile.task == form['condition'])
            ret_task = dy.database.execute(q)
            task_data = []
            for i in ret_task:
                # 翻译status，字典在conf中
                sta0 = i[2]
                stat = conf.stadic[sta0]
                task_data.append({"Task_id":i[0],"File_id":i[1],"Status":stat})
            # 判断是否分析异常
            if (task_data[0]["Status"] == "分析异常"):
            #data = [{"Status": conf.stadic[i[2]], "File_id"} for i in ret]
            # 查询错误msg ↓
                query_err_msg = dy.ErrorMessage.select(dy.ErrorMessage.crash_flag, dy.ErrorMessage.error_message,
                                                           dy.ErrorMessage.error_location, dy.ErrorMessage.error_type) \
                        .where(dy.ErrorMessage.file == task_data[0]['File_id'])
                ret_err_msg = dy.database.execute(query_err_msg)
                err_info = []
                err_row_num = 0
                for i in ret_err_msg:
                    err_row_num += 1
                    tm = {"crash_flag": i[0], "error_msg": i[1], "error_location": i[2], "error_type": i[3]}
                    # crash_flag, error_msg, error_location, error_type = i
                    err_info.append(tm)
                det = {"task_data":task_data,"err_info":err_info,"error_row_num":err_row_num}
                return jsonify(det)
            else:
                det = {"task_data":task_data,"error_row_num":"none","error_code":'success'}
                return jsonify(det)



# @app.route('/error_msg/',methods=['POST'])
# def error_msg():
#     if request.method == "POST":
#         file_id = request.form["file_id"]
#         task_id = request.form["task_id"]
#         db = router.router(task_id)
#         query = db.ErrorMessage.select(db.ErrorMessage.crash_flag, db.ErrorMessage.error_message,
#                                        db.ErrorMessage.error_location, db.ErrorMessage.error_type) \
#                                         .where(db.ErrorMessage.file == file_id)
#         ret = db.database.execute(query)
#         res = {"data":[]}
#         row_num = 0
#         for i in ret:
#             row_num += 1
#             tm = {"crash_flag":i[0], "error_msg":i[1], "error_location":i[2],"error_type":i[3]}
#             #crash_flag, error_msg, error_location, error_type = i
#             res['data'].append(tm)
#
#         if row_num == 0:
#             return "No_error_message"
#         else:
#             res['row_num'] = row_num
#             return jsonify(res)

if __name__ == '__main__':



    app.secret_key = 'whosyourdaddyandgreedyisgood'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0',debug=True)