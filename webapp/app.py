from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': '1132',
    'db': 'threebody',
    'host': '127.0.0.1',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1132@127.0.0.1:5432/threebody'

db = SQLAlchemy(app)

class tasks(db.Model):
   id = db.Column( db.Integer, primary_key = True)
   taskname = db.Column(db.String(100))
   created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class inputs(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   taskid = db.Column(db.Integer, db.ForeignKey('tasks.id'))
   param1 = db.Column(db.Float(20))
   param2 = db.Column(db.Float(20))

class result(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   taskid = db.Column(db.Float, db.ForeignKey('tasks.id'))
   result1 = db.Column(db.Float(20))
   result2 = db.Column(db.Float(20))


@app.route('/')
def show_all():
   return render_template('show_all.html', tasks = tasks.query.all(), inputs = inputs.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['taskname'] or not request.form['id']:
         flash('Please enter all the fields', 'error')
      else:
         task = tasks(request.form['id'],request.form['taskname'],request.form['created'])
         input = inputs(request.form['id'],request.form['taskid'],request.form['param1'],request.form['param2'])
         
         db.session.add(task)
         db.session.add(input)
         db.session.commit()
         
         flash('Task was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')


if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)