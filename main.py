from systemInfo import getSystemInfo, initSystemInfo
from apiRequests import sysBoot, sysinfoUpdate, commandGet, commandUpdate
from hardware import pinSetup, cmdHandler
from interval import Interval
from httpServer import startServer

def getCommandFromServer():
    cmd = commandGet()
    print(cmd)
    if 'id' in cmd:
        cmdId = cmd['id']
        error = cmdHandler(cmdId, cmd.get('type', ''), cmd.get('line', ''))
        if not error:
            commandUpdate(cmdId, 'ok', '')
        else:
            commandUpdate(cmdId, 'fail', 'Unknown command')
    else:
        print('No command')


try:
    print('Starting...')
    pinSetup()
    initSystemInfo()
    systemInfo = getSystemInfo()
    print('Done')
    boot = sysBoot()
    print(boot)
    Interval(boot.get('interval', 10), getCommandFromServer)
    print('Start server')
    startServer()
    print('Finished.')

except Exception as e:
    print('Error:')
    print(e)
