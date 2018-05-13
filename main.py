from systemInfo import getSystemInfo, initSystemInfo
from apiRequests import sysBoot, sysinfoUpdate, commandGet, commandUpdate
# from hardware import pinSetup
from interval import Interval

def getCommandFromServer():
    print(commandGet())

try:
    print('Starting...')
    # pinSetup()
    initSystemInfo()
    systemInfo = getSystemInfo()
    print(systemInfo.getInfoJSON())
    print('Done')
    # print(sysBoot())
    # print(sysinfoUpdate())
    # print(commandGet())
    # print(commandUpdate('turn-on', 'ok', 'message'))
    Interval(sysBoot()['interval'], getCommandFromServer)


except Exception as e:
    print('Error:')
    print(e)
