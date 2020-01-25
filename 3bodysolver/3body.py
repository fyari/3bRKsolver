import json
import requests
import base64
import time
import body_prob as solver

rk_id = 1 

url             = "192.168.17.4:5000/master/"
get_task_url    = url + "get_tasks"
save_result_url = url + "save_result"

params = []

class Task:
    def __init__(self, id , taskname, mx , my , mz):
        self.id = id
        self.name = taskname
        self.mx = mx
        self.my = my
        self.mz = mz
     def __init__(self):
        self.id = 0
        self.name = "taskname"
        self.mx = 1.0
        self.my = 1.0
        self.mz = 1.0
    def print(self):
        print self.id + " " + self.name

def getTasks(rk_id):
    task = Task()
    # task = [id , taskname , mx , my , mz]
    response = requests.get(get_task_url + str(rk_id), verify=False)
    if(response.ok):
        pass
    return task

def saveResult(res):
    response = requests.get(save_result_url + str(res), verify=False)

def rksolver(mx = 2e24, my = 5e30, mz =1e27):
    #get the inputs here from master
    results = solver.threeBody(mx,my,mz)
    return results


if __name__ == "__main__":

    while(True):
        task = getTasks(rk_id)
        # params 
        params = []
        res = rksolver()

        saveResult(res)

        time.sleep(1)
