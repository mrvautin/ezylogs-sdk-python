#!/usr/bin/ python

import os, requests, json, psutil, platform, time, threading
server = "https://ezylogs.com"
minMonitoringInterval = 300000

class configurationClass:
    setup = True

class ThreadJob(threading.Thread):
    def __init__(self,callback,event,interval):
        self.callback = callback
        self.event = event
        self.interval = interval
        super(ThreadJob,self).__init__()

    def run(self):
        while not self.event.wait(self.interval):
            self.callback()

config = configurationClass()

def setup(obj):
    argApiKey = None
    argSystem = None
    argApiKey = obj.get("apiKey")
    argSystem = obj.get("system")

    # Check required args are supplied
    if obj.get("apiKey") == None:
        print('ERROR with configuration object. Missing "apiKey"')
        config.setup = False
        return

    if obj.get("system") == None:
        print('ERROR with configuration object. Missing unique "system" value')
        config.setup = False
        return

    # set the config
    config.apiKey = obj.get("apiKey")
    config.system = obj.get("system")

    # Check the API key etc is correct
    apiKeyCheck = request("/account/auth", {'apiKey': obj.get("apiKey")})

    # Check response
    if apiKeyCheck.status_code != 200:
        config.setup = False
        return

def monitor(interval=30000):
    if interval < minMonitoringInterval:
        print('ERROR with interval. Needs to be {} or greater'.format(minMonitoringInterval))
        return

    event = threading.Event()
    k = ThreadJob(sendUpMonitoring, event, interval / 1000)
    k.start()

def sendUpMonitoring():
    if config.setup == True:
        # Get the process details
        process = psutil.Process(os.getpid())

        content = {
            "pid": os.getpid(),
            "cpu": psutil.cpu_percent(),
            "load": os.getloadavg()[0],
            "platform": platform.system(),
            "processMemory": process.memory_info().rss,
            "processUptime": time.time() - process.create_time(),
            "totalMemory": psutil.virtual_memory().available,
            "freeMemory": psutil.virtual_memory().free,
            "serverUptime": time.time() - psutil.boot_time()
        }

        # Send up monitoring data
        request("/monitor", {
            "apiKey": config.apiKey, 
            "system": config.system,
            "data": content
        })

def sendLog(data, level):
    if config.setup == True:

        request("/log", {
            "apiKey": config.apiKey, 
            "system": config.system,
            "data": data, 
            "level": level
        })

def debug(*argv):
    sendLog(argv, "debug")

def error(*argv):
    sendLog(argv, "error")

def info(*argv):
    sendLog(argv, "info")

def log(*argv):
    sendLog(argv, "log")

def warn(*argv):
    sendLog(argv, "warn")

def request(path, data):
    req = requests.post(server + path, json=data)
    return req