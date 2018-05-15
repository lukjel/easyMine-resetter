from systemInfo import getSystemInfo, initSystemInfo
from apiRequests import sysBoot, sysinfoUpdate, commandGet, commandUpdate
from hardware import pinSetup, powerOn, powerOff
from interval import Interval
from httpServer import startServer

def getCommandFromServer():
    cmd = commandGet()
    print(cmd)
    if cmd['result'] == 'ok':
        if 'commandId' in cmd:
            cmdId = cmd['commandId']
            cmdName = cmd['command']
            cmdPort = cmd['portNo']
            if cmdName == 'power-off':
                powerOff(cmdPort)
                commandUpdate(cmdId, 'ok', '')
            elif cmdName == 'power-on':
                powerOn(cmdPort)
                commandUpdate(cmdId, 'ok', '')
            else:
                commandUpdate(cmdId, 'fail', 'Unknown command')
        else:
            print('No command')
    else:
        print('Server error')


try:
    print('Starting...')
    pinSetup()
    initSystemInfo()
    systemInfo = getSystemInfo()
    print('Done')
    Interval(sysBoot()['interval'], getCommandFromServer)
    startServer()

except Exception as e:
    print('Error:')
    print(e)
