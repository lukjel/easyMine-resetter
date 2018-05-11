from systemInfo import getSystemInfo, initSystemInfo

try:
    print('Starting...')
    initSystemInfo()
    systemInfo = getSystemInfo()
    print(systemInfo.getInfoJSON())
    print('Done')
except Exception as e:
    print('Error:')
    print(e)
