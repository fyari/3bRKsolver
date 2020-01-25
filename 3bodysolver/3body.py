import json
import requests
import base64
import time

rk_id = 1 

url             = "192.168.17.4/api/v1/"
get_task_url    = url + "gettask"
save_result_url = url + "saveresult"

params = []

def getTasks(rk_id):
    response = requests.get(get_task_url + str(rk_id), verify=False)
    if(response.ok):
        a=[]
def saveResult(res):
    response = requests.get(save_result_url + str(res), verify=False)

def rksolver():
    pass


if __name__ == "__main__":

    while(True):
        task = getTasks(rk_id)
        # params 
        params = []
        res = rksolver()

        saveResult(res)

        time.sleep(1)
