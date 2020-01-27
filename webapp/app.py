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
app.config['SECRET_KEY'] = 'random string'


db = SQLAlchemy(app)


class task(db.Model): 
   id = db.Column(db.Integer, primary_key = True)
   taskname = db.Column(db.String(100))
   created = db.Column(db.DateTime, default=datetime.utcnow)
   status = db.Column(db.Integer,default = 0)
   active = db.Column(db.Integer,default = 0)


class io(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   task_id = db.Column(db.Integer)
   category = db.Column(db.Integer,default = 0)
   symbol = db.Column(db.String(20))
   value  = db.Column(db.Float(20))

   
   
@app.route('/')
def show_all():
   #taskid = 1
   #return redirect(url_for('show_all'))
   #io.query.filter_by(category=0).filter_by(task_id=1).all(), io.query.filter_by(category=1).filter_by(task_id=1).all()
   return render_template('show.html', data = [task.query.all() ] )

@app.route('/show/<int:task_id>')
def index(task_id):
   taskid = task_id
   #return request.base_url
   return render_template('show_all.html', data = [taskid  , task.query.all(), io.query.filter_by(category=0).filter_by(task_id=taskid).all(), io.query.filter_by(category=1).filter_by(task_id=taskid).all() ] )


@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['taskname']:
         flash('Please enter all the fields', 'error')
      else:
         
         taskobj = task(taskname = request.form['taskname'])
         #taskobj =  request.form['taskname']
         db.session.add(taskobj)
         db.session.commit()

         mytask = task.query.filter_by(taskname=request.form['taskname']).first()

         
         for k, v in request.form.iteritems():
            #print k , v
            if k == "taskname":
               continue
            else:
               ios = io(task_id = mytask.id)
               ios.symbol = k
               ios.value = float(v)
               ios.category = 0
               db.session.add(ios)
               db.session.commit()
         
         
         mytask.active = 1
         
         db.session.merge(mytask)
         db.session.commit()


         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')


if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)