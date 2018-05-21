from systemInfo import getSystemInfo, initSystemInfo
from apiRequests import sysBoot, sysinfoUpdate, commandGet, commandUpdate
from hardware import pinSetup, cmdHandler
from interval import Interval
from httpServer import startServer

def getCommandFromServer():
    cmd = commandGet()
    print(cmd)
    if cmd['result'] == 'ok':
        if 'commandId' in cmd:
            cmdId = cmd['commandId']
            error = cmdHandler(cmdId, cmd['command'], cmd['portNo'])
            if error:
                commandUpdate(cmdId, 'fail', 'Unknown command')
            else:
                commandUpdate(cmdId, 'ok', '')
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
    print('Start server')
    startServer()
    print('Finished.')

except Exception as e:
    print('Error:')
    print(e)
