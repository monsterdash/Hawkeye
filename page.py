import  pymysql,conf


#query={}
# array = ['page','task_id','file_id','status']


def parse(query):
    if query != {}:
        task_id_req = 'task_id' + query['task_id']
        file_id_req = 'file_id' + query['file_id']
        status_req = 'status' + query['status']
        order = 'order' +query['order']
        desc = query ['desc']
        condition = task_id_req + file_id_req + status_req + order + desc
        return condition

def page_number(query):
        return query['page']

def pager(condition,page_number):
    request = 'select task_id,file_id,status from taskid_file a left join file b on b.id=a.file_id\
               where'+ condition + 'order by task_id '
    PAGE_COUNT_SQL = "select count(*) from " + request
    pager = "SELECT TOP " + conf.ROW_NUM + " * FROM \
        ( \
            SELECT ROW_NUMBER() OVER (ORDER BY id) AS RowNumber,* FROM \
            ( " + request + " )\
        )   as A \
        WHERE RowNumber > " + conf.ROW_NUM + "*(" + page_number +"-1) "
    conn = pymysql.connect(host='192.168.230.128', port=3306,user='root', passwd='root', db='mobei3')
    cur = conn.cursor()
    cur.execute(PAGE_COUNT_SQL)
    for i in cur:
        PAGE_COUNT = "%d" %i[0]



    cur.execute(request)

