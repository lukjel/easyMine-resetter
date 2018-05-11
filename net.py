import os
import shellUtils
import socket, fcntl, struct, binascii, re, uuid
import env
from multiprocessing import Pool

instance = None

def getNetworkUtil():
    global instance;
    if instance is None:
        instance = NetUtil()

    return instance


class NetUtil:
    def __init__(self):
        self.ip_local = self.getIp()
        self.interfaces = []
        self.TCP_PROBE_TIMEOUT = env.RUNTIME_PARAMETERS['TCP_PROBE_TIMEOUT']
        self.arp_table = {}

    def getMac(self, interface=None):
        if not interface:
            return self.getActiveInterfaceMac()
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.2)
            info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s',  bytes(interface[:15], 'utf-8')))
            s.close()
            return ''.join(l + ':' * (n % 2 == 1) for n, l in enumerate(binascii.hexlify(info[18:24]).decode('utf-8')))[:-1]
        except:
            s.close()
            return None

    def getActiveInterfaceMac(self):
        return (':'.join(re.findall('..', '%012x' % uuid.getnode())))

    def isIP(self, s):
        a = s.split('.')
        if len(a) != 4:
            return False
        for x in a:
            if not x.isdigit():
                return False
            i = int(x)
            if i < 0 or i > 255:
                return False
        return True

    def getIp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ipv4 = s.getsockname()[0]
        s.close()
        return ipv4

    def clearArpTable(self):
        self.arp_table = {}

    def _refreshArpTableParseLine(self, line):
        tmp = line[:-1].split()
        if tmp[0] not in self.arp_table and tmp[2].count(':') > 4:
            self.arp_table[tmp[0]] = tmp[2]

    def _refreshArpTable(self):
        with shellUtils.subprocessRun(['arp']) as proc:
            shellUtils.watchProcessOutput(proc, self._refreshArpTableParseLine)

    def getMacForHost(self, ip):
        if self.arp_table == {}:
            self._refreshArpTable()

        if ip in self.arp_table:
            return self.arp_table[ip]
        return None

    def getDataViaTCPSocket(self, hostport, payload='{}', timeout=2):
        if type(payload) is list or type(payload) is dict:
            payload = json.dumps(payload)
        elif type(payload) is not str:
            return None
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            s.connect(hostport)
            s.send(bytes(payload, 'utf-8'))
            chunks = []
            while True:
                chunk = s.recv(1024)
                if chunk == b'':
                    break
                chunks.append(chunk)
            return b''.join(chunks).decode().rstrip('\0')
        except Exception as e:
            return None
        finally:
            s.close()


    def tcpProbe(self, hostport):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.settimeout(self.TCP_PROBE_TIMEOUT)
            res = s.connect_ex(hostport)
            if res == 0:
                s.close()
                return hostport[0]
        except:
            pass
        finally:
            s.close()
        return None

    def scanLocalSubnet(self, my_ip=None, port=4028, threads=32):
        if not my_ip:
            my_ip = self.ip_local
        my_subnet = my_ip[:my_ip.rindex('.')]
        tcp_probe_list = map(lambda i: ((my_subnet + '.' + str(i)), port), range(1, 255))
        with Pool(threads) as pool:
            results = pool.map(self.tcpProbe, tcp_probe_list)
        active = filter(lambda ip: ip !=None, results)
        return list(active)
