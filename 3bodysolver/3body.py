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

def getTasks(rk_id):
    response = requests.get(get_task_url + str(rk_id), verify=False)
    if(response.ok):
        a=[]
def saveResult(res):
    response = requests.get(save_result_url + str(res), verify=False)

def rksolver():
    #get the inputs here from master
    results = solver.threeBody(2e24,5e30,1e27)
    #save results, results is a list of 4 elements


if __name__ == "__main__":

    while(True):
        task = getTasks(rk_id)
        # params 
        params = []
        res = rksolver()

        saveResult(res)

        time.sleep(1)
