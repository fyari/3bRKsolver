from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class tasks(db.Model):
   id = db.Column( db.Integer, primary_key = True)
   taskname = db.Column(db.String(100))
   created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
   status = db.Column(db.String(50))
      

class inputs(db.Model):
   id = db.Column('input_id', db.Integer, primary_key = True)
   taskid= db.Column(db.Integer, db.ForeignKey('tasks.id'))
   param1 = db.Column(db.Float(20))
   param2 = db.Column(db.Float(20))
   param3 = db.Column(db.Float(20))
   

class result(db.Model):
   id = db.Column('results', db.Integer, primary_key = True)
   taskid = db.Column(db.Integer ,  db.ForeignKey('tasks.id'))
   result1 = db.Column(db.Float(20))
   result2 = db.Column(db.Float(20))
   result3 = db.Column(db.Float(20))
   


@app.route('/')
def show_all():
   return render_template('show_all.html', tasks = tasks.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['name']:
         flash('Please enter all the fields', 'error')
      else:
         task = tasks(request.form['name'])
         
         db.session.add(task)
         db.session.commit()
         
         flash('Task was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')

now = datetime.datetime.now()
print ("Current date and time : ")
print (now.strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
