import json
import requests
import base64
import time
import solve_3body as solver

 

url             = "http://192.168.17.4:5000/"
get_task_url    = url + "task/"
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

	def getAllVars(self):
		return [self.mx, self.my, self.mz, self.x1, self.y1, self.x2, self.y2, self.x3, self.y3, self.vx1, self.vy1, self.vx2, self.vy2, self.vx3, self.vy3]
	def __str__(self):
		l = [self.id, self.name, self.mx, self.my, self.mz, self.x1, self.y1, self.x2, self.y2, self.x3, self.y3, self.vx1, self.vy1, self.vx2, self.vy2, self.vx3, self.vy3]
		return str(l)


def getTasks(rk_id):
	response = requests.get(get_task_url + str(rk_id), verify=False)
	if response.ok:
		#print response
		#print response.url
		#print response.json()
		#print response.json()["id"]
		tj = response.json()
		task = Task(tj['id'], tj['taskname'], tj['m1'], tj['m2'], tj['m3'], tj['m1x'], tj['m1y'], tj['m2x'], tj['m2y'], tj['m3x'], tj['m3y'], tj['m1vx'], tj['m1vy'], tj['m2vx'], tj['m2vy'], tj['m3vx'], tj['m3vy'])
		return task
	if not response.ok:
		return -1
		#print response.url
		
	
	
	

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
    results = solver.threeBody(*inputs)
    return results

def setStatus(task,status):

	res_ready_url = set_status_url + "/{}/{}".format(task.id,status)
	
	while(True):
		response = requests.get( res_ready_url, verify=False)
		if response.ok:
			print('result ready status sent')
			break

def registerRKSolver():
	response = requests.get(register_rk_url, verify=False)
	#print response
	#print response.url
	#print response.json()
	#print response.json()["id"]
	if not response.ok:
		print ("ERROR : registered rk solver ... ")
	if response.ok:
		return response.json()["id"]

		

if __name__ == "__main__":
	time.sleep(20)
	rk_id = registerRKSolver()
	print("RKSolver Registered : " , str(rk_id))

	while(True):

		task = getTasks(rk_id)
		if task == -1:
			print("ERROR : Getting Task ... , MAYBE NO TASK AVAILABLE " )
			time.sleep(1)
			continue


		print (task)

		params = []
		print ("calculating result ...\n")
		res = rksolver(task.getAllVars())
		print ("result : " , res)
		print ("saving results ... \n")
		saveResult(task,res)
		print ("setting task status to 2")
		setStatus(task,2)
		print ("tired , ... sleeping ....")
		time.sleep(1)
	
