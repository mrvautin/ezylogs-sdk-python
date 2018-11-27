import httplib, json, psutil, datetime
server = "https://ezylogs.com"

class configurationClass:
    setup = True

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
    apiKeyCheck = request("/account/auth", {"apiKey": obj.get("apiKey")})

    # Check response
    if apiKeyCheck.status != 200:
        config.setup = False
        return

def sendUpMonitoring():
    if config.setup == True:
        # content = {
        #     "pid": monitorData.pid,
        #     "cpu": monitorData.cpu,
        #     "load": os.loadavg()[0],
        #     "platform": os.platform(),
        #     "processMemory": process.memoryUsage().rss,
        #     "processUptime": monitorData.elapsed,
        #     "totalMemory": os.totalmem(),
        #     "freeMemory": os.freemem(),
        #     "serverUptime": os.uptime() * 1000
        # }
        print(psutil.virtual_memory())

        request("/monitoring", {
            "apiKey": config.apiKey, 
            "system": config.system,
            "data": {}, 
            "timestamp": datetime.datetime.utcnow().isoformat()
        })

def sendLog(data, level):
    print('data', data)
    if config.setup == True:
        if type(data) is dict:
            print('in here')
            data = json.dumps(data)

        test = request("/log", {
            "apiKey": config.apiKey, 
            "system": config.system,
            "data": data, 
            "level": level,
            "timestamp": datetime.datetime.utcnow().isoformat()
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
    params = json.dumps(data)
    print("params", params)
    headers = { 
        "Content-type": "application/json",
        "Accept": "application/json"
    }
    conn = httplib.HTTPConnection("gatehouseg1.stgeorge.com.au", "8080")
    conn.request("POST", server + path, headers=headers, body=params)
    return conn.getresponse()