import requests
import json
import env
from systemInfo import getSystemInfo

def statusHandler(response):
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    elif response.status_code == 400:
        return 'Bad Request'
    else:
        return response.status_code



def sysBoot():
    url = env.URL_BASE + '/v1/controller/boot'
    sysInfo = getSystemInfo()
    payload = sysInfo.getInfoJSON()
    r = requests.post(url, data=json.dumps(payload))
    return statusHandler(r)


def sysinfoUpdate():
    url = env.URL_BASE + '/v1/controller/sysinfo/update'
    sysInfo = getSystemInfo()
    payload = {
        'id': str(sysInfo.hardwarehash),
        'ip': str(sysInfo.network.ip_local),
        'upgrade': str(sysInfo.VERSION)
    }
    r = requests.post(url, data=json.dumps(payload))
    return statusHandler(r)


def commandGet():
    url = env.URL_BASE + '/v1/controller/command/get'
    sysInfo = getSystemInfo()
    payload = {
        'id': str(sysInfo.hardwarehash)
    }
    r = requests.post(url, data=json.dumps(payload))
    return statusHandler(r)


def commandUpdate(commandId, result, message):
    url = env.URL_BASE + '/v1/controller/command/update'
    sysInfo = getSystemInfo()
    payload = {
        'id': str(sysInfo.hardwarehash),
        'commandId': str(commandId),
        'result': str(result),
        'message': str(message)
    }
    r = requests.post(url, data=json.dumps(payload))
    return statusHandler(r)

def commandRegister(token):
    url = env.URL_BASE + '/v1/controller/register'
    sysInfo = getSystemInfo()
    payload = sysInfo.getInfoJSON()
    payload['token'] = token
    r = requests.post(url, data=json.dumps(payload))
    return statusHandler(r)
