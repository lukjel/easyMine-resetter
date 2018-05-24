from net import getNetworkUtil
import hashlib, sys, env
import json

class Identification():
    def __init__(self):
        self.VENDOR = env.VENDOR
        self.VERSION = env.VERSION
        self.MODEL = env.MODEL
        self.LINES = env.LINES
        self.SUPPORTED_COMMANDS = env.SUPPORTED_COMMANDS
        self.network = getNetworkUtil()
        self.mac1 = self.getMac('eth0')
        self.mac2 = self.getMac('wlan0')
        self.hardwareid = self.getHardwareId()
        self.hardwarehash = self.getHardwarehash()

    def getHardwarehash(self):
        return hashlib.sha256(bytearray(str(self.VENDOR + self.VERSION + self.MODEL + self.mac1 + self.mac2 + self.hardwareid), 'utf-8')).hexdigest()

    def getInfoJSON(self):
        res = {
            'ip': str(self.network.ip_local),
            'id': str(self.hardwarehash),
            'vendor': str(self.VENDOR),
            'version': str(self.VERSION),
            'model': str(self.MODEL),
            'commands': self.SUPPORTED_COMMANDS,
            'lines': self.LINES
        }

        return json.loads(json.dumps(res))

    def getHardwareId(self):
        try:
            with open('/proc/cpuinfo','r') as f:
                for line in f:
                    if 'Serial' in line and len(line) > 20:
                        return line[len(line) - 17:-1]
        except:
            pass
        return '0000000000000000'

    def getMac(self, iface):
        try:
            mac = self.network.getMac(iface)
            if mac:
                return mac
        except:
            pass
        return '??:??:??:??:??:??'

systemInfo = None

def getSystemInfo():
    global systemInfo
    return systemInfo

def initSystemInfo():
    global systemInfo
    if systemInfo is None:
        systemInfo = Identification()
    return systemInfo
