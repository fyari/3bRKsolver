import json
import requests
import base64
import time
import solve_3body as solver

rk_id = 1 

url             = "http://127.0.0.1:5000/"
get_task_url    = url + "task"
save_result_url = url + "save"
register_rk_url = url + "registerrk"
set_status_url  = url + "status"
status_result_ready = 2


class Task:
	def __init__(self, id , taskname, M1 , M2 , M3, x1, y1, x2, y2, x3, y3, vx1, vy1, vx2, vy2, vx3, vy3):
		self.id = id
		self.name = taskname
		self.mx = M1
		self.my = M2
		self.mz = M3
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.x3 = x3
		self.y3 = y3
		self.vx1 = vx1
		self.vy1 = vy1
		self.vx2 = vx2
		self.vy2 = vy2
		self.vx3 = vx3
		self.vy3 = vy3
	def __init__(self):
		self.id = 0
		self.name = "taskname"
		self.mx = 1.0
		self.my = 1.0
		self.mz = 1.0
		self.x1 = 1.0
		self.y1 = 1.0
		self.x2 = 0.0
		self.y2 = 0.0
		self.x3 = 2.0
		self.y3 = 2.0
		self.vx1 = 0.0
		self.vy1 = 0.0
		self.vx2 = 0.0
		self.vy2 = 0.0
		self.vx3 = 0.0
		self.vy3 = 0.0

	def getAllVars(self):
		return [self.mx, self.my, self.mz, self.x1, self.y1, self.x2, self.y2, self.x3, self.y3, self.vx1, self.vy1, self.vx2, self.vy2, self.vx3, self.vy3]

	def print(self):
		print (self.id + " " + self.name)

def getTasks(rk_id):
	while(True):
		response = requests.get(get_task_url + str(rk_id), verify=False)
		if response.ok:
			print('task fetched from master')
			break
	tj = response.json()
	task = Task(tj['id'], tj['taskname'], tj['m1'], tj['m2'], tj['m3'], tj['m1x'], tj['m1y'], tj['m2x'], tj['m2y'], tj['m3x'], tj['m3y'], tj['m1vx'], tj['m1vy'], tj['m2vx'], tj['m2vy'], tj['m3vx'], tj['m3vy'])
	
	return task

def saveResult(task,res):
    #response = requests.get(save_result_url + str(res), verify=False)
	for i in range(0,len(res)):
		r_string = "/{}/{}/{}".format(task.id, i, res[i])
		full_url =  save_result_url + r_string

		while(True):
			response = requests.get(full_url, verify=False)
			if response.ok:
				print("result saved")
				break
		print(response.json())
		time.sleep(0.5)

def rksolver(inputs):
    #get the inputs here from master
    results = solver.threeBody(inputs)
    return results

def setStatus(task,status):

	res_ready_url = set_status_url + "/{}/{}".format(task.id,status)
	
	while(True):
		response = requests.get( res_ready_url, verify=False)
		if response.ok:
			print('result ready status sent')
			break
def registerRKSolver():

	while(True):
		response = requests.get(register_rk_url, verify=False)
		if response.ok:
			print('registered rk solver')
			break
	rk_id_json = response.json()
	return rk_id_jason["id"]	

if __name__ == "__main__":

	rk_id = registerRKSolver()
	
	while(True):
		task = getTasks(rk_id)
		# params 
		params = []
		res = rksolver(task.getAllVars())
		
		saveResult(task,res)
		setStatus(task,2)

		time.sleep(1)
