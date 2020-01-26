from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
#from flask_sqlalchemy import SQLAlchemy
#import datetime

from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

app = Flask(__name__)
api = Api(app)


#parser = reqparse.RequestParser()
#parser.add_argument('task')

#app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1132@127.0.0.1:5432/threebody'

engine = create_engine('postgresql://postgres:postgres@localhost/threebody')
try:
    con = engine.connect()
        
except Exception:
    print("FATAL ERROR IN MASTER NODE !!! ")

RKSOLVERS = {}

def registerSolver():
    id = 0
    if len(RKSOLVERS) == 0:
        RKSOLVERS[1] = 'RK_1'
        id = 1
    else:  
        id = RKSOLVERS.keys()[-1] + 1
        RKSOLVERS[id] = 'RK_' + str(id)
    return  {'id' : id }


def getTaskID(con,taskname):
    d = {}
    d['taskname'] = taskname
    rs = con.execute(text("""select * from task where taskname = :taskname """), **d)
    #print rss.fetchone()
    for iter in rs:
        id = iter[0]
    return id

def setTaskStatus(taskname , status):
    d = {}
    d['taskname'] = taskname
    d['s'] = status
    
    rs = con.execute(text("""update task set status = :s where taskname = :taskname """), **d)


def saveSymbolResult(con , taskname , symbol , value):
    d = {}
    d['taskname'] = taskname
    d['s'] = symbol
    d['v'] = value
    d['id'] = getTaskID(con,taskname)
    
    rs = con.execute(text("""insert into io (task_id , type , symbol , value ) values (:id , 1 , :s , :v) """), **d)


def getTaskInputs(taskname):
    d = {}
    d['taskname'] = taskname
    d['id'] = getTaskID(con,taskname)

    rs = con.execute(text("""select symbol , value from io where task_id = :id and type = 0; """), **d)
    rss = rs.fetchall()
    # error NoneTpe object should be solved
    if (rss):
        for i in rss:
            d[i[0]] = i[1]
    else:
        return {'error':'no task'}
    #print d
    return d



def getNewTask():
    task = []
    rs = con.execute("select * from task where status = 0 ")
    # error NoneTpe object should be solved
    if (rs):
        job = rs.fetchone() 
        for iter in job:
            task.append(iter)
    
        #rs = con.execute(text("""update task set status = :  """), **d)
        #for iter in job:
        #    task.append(iter[0])
    else:
        #print task
        return {'error':'no task'}
    #print task
    return {'id':task[0] , 'taskname':task[1] }



def shutdown():
    con.close()

class RKSolver(Resource):
    def get(self):
        #abort_if_todo_doesnt_exist(todo_id)
        return registerSolver()

class Task(Resource):
    def get(self,rk_id):
        # get new task , get inputs , (set task status = 1 , return json to rk )
        d = getNewTask()
        s = getTaskInputs(d['taskname'])
        setTaskStatus(d['taskname'],1)
        print s
        return s
        


api.add_resource(RKSolver, '/registerrk')
#api.add_resource(Task, '/task')
api.add_resource(Task, '/task/<rk_id>')
#api.add_resource(Results, '/save/<taskname>/<symbol>/<value>')

if __name__ == '__main__':
    engine = create_engine('postgresql://postgres:postgres@localhost/threebody')
    
   

    app.run(debug=True)
    #getTaskInputs('task 1')
    #rk = RKSolver(con)  
    #rk.show()
    #rk.registerSolver()
    #rk.show()
    #getNewTasks(con)
    #print str(registerSolver())
    #print str(registerSolver())

    #print saveTask(con , 'my task 400')
    #print getTaskID(con ,"my task 400")

    #saveSymbolResult(con,"my task 4","m1x",101.01)