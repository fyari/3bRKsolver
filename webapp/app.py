from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'threebody',
    'host': '127.0.0.1',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/threebody'


db = SQLAlchemy(app)

class task(db.Model): 
   id = db.Column(db.Integer, primary_key = True)
   taskname = db.Column(db.String(100))
   created = db.Column(db.DateTime, default=datetime.utcnow)
   status = db.Column(db.Integer,default = 0)
   active = db.Column(db.Integer,default = 1)

def __init__(self,taskname, created,status,active):
   self.taskname = taskname
   self.created = created
   self.status = status
   self.active = active
  
class io(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   task_id = db.Column(db.Integer)
   category = db.Column(db.Integer,default = 0)
   symbol = db.Column(db.String(20))
   value  = db.Column(db.Float(20))
   #m1 = db.Column(db.Float(50))
   #m2 = db.Column(db.Float(50))
   #m3 = db.Column(db.Float(50))
   #x1 = db.Column(db.Float(50))
   #y1 = db.Column(db.Float(50))
   #vx1 = db.Column(db.Float(50))
   #vy1 = db.Column(db.Float(50))
   #x2 = db.Column(db.Float(50))
   #y2 = db.Column(db.Float(50))
   #vx2 = db.Column(db.Float(50))
   #vy2 = db.Column(db.Float(50))
   #x3 = db.Column(db.Float(50))
   #y3 = db.Column(db.Float(50))
   #vx3 = db.Column(db.Float(50))
   #vy3 = db.Column(db.Float(50))


def __init__(self, task_id, category):
   self.task_id = task_id
   self.category = category
   self.m1 = m1
   self.m2 = m2
   self.m3 = m3
   self.x1 = x1
   self.y1 = y1
   self.vx1 = vx1
   self.vy1 = vy1
   self.x2 = x2
   self.y2 = y2
   self.vx2 = vx2
   self.vy2 = vy2
   self.x3 = x3
   self.y3 = y3
   self.vx3 = vx3
   self.vy3 = vy3
   
@app.route('/')
def show_all():
   taskid = 1
   return render_template('show_all.html', data = [taskid  , task.query.all(), io.query.filter_by(category=0).filter_by(task_id=1).all(), io.query.filter_by(category=1).filter_by(task_id=1).all() ] )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['taskname']:
         flash('Please enter all the fields', 'error')
      else:
         
         #ios = io(request.form['m1'])
         
         #ios = io(m1 = request.form['m1'],m2 = request.form['m2'],m3 = request.form['m3'],x1 = request.form['x1'],y1 = request.form['y1'],vx1 = request.form['vx1'],vy1 = request.form['vy1'],x2 = request.form['x2'],y2 = request.form['y2'],vx2 = request.form['vx2'],vy2 = request.form['vy2'],x3 = request.form['x3'],y3 = request.form['y3'],vx3 = request.form['vx3'],vy3 = request.form['vy3']  )
         db.session.add(ios)
         db.session.commit()
         taskobj = task(taskname = request.form['taskname'])
         db.session.add(taskobj)
         db.session.commit()

         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')


if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)