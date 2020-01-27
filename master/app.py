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
"""
def createdb(db = 'threebody'):
    d = {}
    d['db'] = db
    rs = con.execute(text(create database :db ;), **d)
    print "DATABASE CREATED ...\n"
"""
engine = create_engine('postgresql://postgres:postgres@192.168.17.3:5432/')

try:
    con = engine.connect()
        
except Exception:
    print("FATAL ERROR IN MASTER NODE !!! ")
    #engine = create_engine('postgresql://postgres:postgres@192.168.17.3:5432')
    #con = engine.connect()
    #createdb('threebody')

    #print("FATAL ERROR IN MASTER NODE !!! ")
#del(engine)
"""
engine = create_engine('postgresql://postgres:postgres@192.168.17.3:5432/threebody')
try:
    con = engine.connect()
        
except Exception:
    print("FATAL ERROR IN MASTER NODE !!! ")
"""
def tablesExist(tablename):
    d = {}
    d['tn'] = tablename
    rs = con.execute(text("""select exists ( select 1 from information_schema.tables where table_name = :tn ) """), **d)
    for iter in rs:
        return iter[0]



def craeteTable(tablename):
    d = {}
    if tablename == 'task':
        rs = con.execute(text("""create table task (id serial primary key ,taskname varchar(50) unique not null, created timestamp not null DEFAULT CURRENT_TIMESTAMP,status integer not null DEFAULT 0, active integer not null DEFAULT 0);"""), **d)
        print "TABLE task CREATED ...\n"
    if tablename == 'io':
        rs = con.execute(text("""create table io (id serial primary key ,task_id integer not null,category integer not null DEFAULT 0,symbol varchar(10) not null,value double precision ,FOREIGN KEY (task_id) REFERENCES task(id)); """), **d)
        print "TABLE io CREATED ...\n"

def checktablesExists():
    d = {}

    if not tablesExist('task'):
        print "TABLE task DOES NOT EXISTS , ATTEMPTING TO CREATE ... "
        craeteTable('task')
    if not tablesExist('io'):
        print "TABLE io DOES NOT EXISTS , ATTEMPTING TO CREATE ... "
        craeteTable('io')
    if tablesExist('task') and tablesExist('io'):
        print 'TABLES task , io EXISTS ... '


RKSOLVERS = {}

def registerSolver():
    id = 0
    if len(RKSOLVERS) == 0:
        RKSOLVERS[1] = '0'
        id = 1
    else:  
        id = RKSOLVERS.keys()[-1] + 1
        RKSOLVERS[id] = 0
    return  {'id' : id }

def setSolverTask(rk_id,taskid):
    RKSOLVERS[rk_id] = taskid
def getSolverTask(rk_id):
    return RKSOLVERS[rk_id] 
def checkTaskAssigned(taskid):
    pass



def getTaskID(taskname):
    d = {}
    d['taskname'] = taskname
    rs = con.execute(text("""select * from task where taskname = :taskname """), **d)
    rss = rs.fetchone()
    id = rss[0]
    return id

def setTaskStatus(taskid , status):
    d = {}
    d['id'] = int(taskid)
    d['sts'] = int(status)
    #print d
    #trans = con.begin()
    try:
        rs = con.execute(text("""update task set status = :sts where id = :id """), **d)
        return {'status':'OK'}
        #trans.commit()
    except:
        #trans.rollback()
        #raise
        return {'status':'ERROR'}


def saveSymbolResult(taskid , symbol , value):
    d = {}
    d['id'] = taskid
    d['s'] = symbol
    d['v'] = float(value)
    #d['id'] = getTaskID(con,taskname)
    #trans = con.begin()
    try:
        rs = con.execute(text("""insert into io (task_id , category , symbol , value ) values (:id , 1 , :s , :v) """), **d)
        #trans.commit()
        return {'status':'OK'}
    except:
        #trans.rollback()
        #raise
        return {'status':'ERROR'}

def getTaskInputs(taskname):
    d = {}
    d['taskname'] = taskname
    d['id'] = getTaskID(taskname)
    #print d['id']
    rs = con.execute(text("""select symbol , value from io where task_id = :id and category = 0; """), **d)
    rss = rs.fetchall()
    # error NoneTpe object should be solved
    if rss == None:
        return {'error':'NOINPUTS'}
    try:
        for i in rss:
            d[i[0]] = i[1]
    except:
        return {'error':'NOINPUTS'}
    return d



def getNewTask():
    task = []
    # task should be activate by webapp after inserting all inputs
    rs = con.execute("select * from task where status = 0 and active = 1 ")
    # error NoneTpe object should be solved
    if (rs):
        job = rs.fetchone() 
        try:    
            for iter in job:
                task.append(iter)
        except:
            return {'id':-1}
 
    else:
        #print task
        return {'id':-1}
    #print task
    return {'id':task[0] , 'taskname':task[1] }



class RKSolver(Resource):
    def get(self):
        return registerSolver()

class Task(Resource):
    def get(self,rk_id):
        # get new task , get inputs , (set task status = 1 , return json to rk )
        d = getNewTask()
        if d['id'] == -1 :
            return {'status':'NOTASK'}
        s = getTaskInputs(d['taskname'])
        setTaskStatus(d['id'],1)
        return s

        
class Result(Resource):
    def get(self,taskid , symbol , value):
        d = saveSymbolResult(taskid,symbol,value)
        return d

class Status(Resource):
    def get(self,taskid, status):
        d = setTaskStatus(taskid , status)
        return d

api.add_resource(RKSolver, '/registerrk')
#api.add_resource(Task, '/task')
api.add_resource(Task, '/task/<rk_id>')
#api.add_resource(Result, '/save/<taskname>/<symbol>/<value>')
api.add_resource(Result, '/save/<taskid>/<symbol>/<value>')
api.add_resource(Status, '/status/<taskid>/<status>')

if __name__ == '__main__':
    #createdb('threebody')
    checktablesExists()
    app.run(debug=True)
 
