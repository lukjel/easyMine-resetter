import subprocess
import threading

def decodeBytes(textBytes):
    if textBytes:
        try:
            return textBytes.decode('utf-8')
        except Exception as e:
            return textBytes.decode('ascii')
    return None

def watchProcessOutputNewThread(process, callback=None):
    threading.Thread(target=watchProcessOutput, args=(process, callback)).start()
    return process

def watchProcessOutput(process, callback=None, exitCodeCallback=None):
    try:
        while process.returncode is None:
            for line in process.stdout:
                line = decodeBytes(line)
                #print(" ====> " + line, end='', flush=True)
                if callback is not None:
                    callback(line)
            process.poll()
        if exitCodeCallback is not None:
            exitCodeCallback(process.returncode)
    finally:
        process.kill()


def runShellCommand(command, env=None):
    opened = subprocess.Popen(["stdbuf","-o0"] + command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    return opened

def subprocessRun(array, env=None):
    opened = subprocess.Popen(array , stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    return opened

def printLine(line):
    print(line)

def printOutput(proc):
    return watchProcessOutput(proc, printLine)
