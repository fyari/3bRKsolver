#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request

rk = []
# rk = (rk_id,task_id)
# rk [(1,20),(2,21)]

#db

app = Flask(__name__)

db = [("")]

tasks = [
    {
        'id': 1,
        'name': u'my task 1',
        'created': u'10102020', 
        'status': 'result_ready'
    },
    {
        'id': 2,
        'name': u'my task 2',
        'created': u'10102020', 
        'status': 'result_not_ready'
    },
    {
        'id': 3,
        'name': u'my task 3',
        'created': u'10102020', 
        'status': 'not_computed'
    },
    {
        'id': 4,
        'name': u'my task 4',
        'created': u'10102020', 
        'status': 'not_computed'
    }
]

# models : tasks , result , inputs

def get_all_tasks():
    return []


def get_not_computed_tasks():
    return [1]


@app.route('/master/save_result/<float:x>/<float:y>', methods=['GET'])
def save_result(x,y):
    # read result from incoming json
    # save result in database
    # update rk if needed
    return jsonify({'savedx': x,'savedy':y})


@app.route('/master/get_tasks/<int:rk_id>', methods=['GET'])
def get_tasks(rk_id):
    task = get_not_computed_tasks()
    if len(task) == 0:
	return jsonify({'task':1})
    elif len(task) == 1:
	return jsonify(tasks[1])
    else:
    #decide which task to send---
    #update rk.append() or rk.update()
    # send jesonify task to rk 
	return jsonify({'tasks': tasks})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
