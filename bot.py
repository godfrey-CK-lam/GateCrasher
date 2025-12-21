import argparse
import http.client
import json
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('start', type=str)
parser.add_argument('end', type=str)
args = parser.parse_args()

start = '\"' + args.start + '\"'
end = '\"' + args.end + '\"'

conn = http.client.HTTPSConnection("esi.evetech.net")

headers = {
        'Accept-Language': "en",
        'If-None-Match': "",
        'X-Compatibility-Date': "2025-12-16", #time.strftime("%Y-%m-%d")
        'X-Tenant': "",
        'Content-Type': "application/json",
        'Accept': "application/json"
    }
# parse a system name to the id
def parseName(system):
    payload = "[\n" + system + "\n]"


    conn.request("POST", "/universe/ids", payload, headers)

    res = conn.getresponse()
    allData = res.read()
    parseData = json.loads(allData)    

    data = parseData.get("systems")
    return data[0]["id"]

  
# parse a system ID to a name
def parseID(id):
    payload = "[\n  "+ str(id) +"\n]"

    conn.request("POST", "/universe/names", payload, headers)

    res = conn.getresponse()
    data = res.read()
    parseData = json.loads(data)    
    return parseData[0]['name']

def getInfo(id):
    conn.request("GET", "/universe/systems/" + str(id), headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    parseData = json.loads(data)   
    
 
    
    return [parseData['name'], round(parseData['security_status'], 1), getKills(id)]

def getKills(id):
    conn.request("GET", "/universe/system_kills", headers=headers)

    res = conn.getresponse()
    data = res.read()
    parseData = json.loads(data)  

    kills = 0
    result = next((obj for obj in parseData if obj["system_id"] == id),0)
    print(id)
    # print(parseData)

    print(result)

    
    
    if result:
        kills = result["pod_kills"] + result["ship_kills"]
  
    return kills




#print(start)
startid = parseName(start)
endid = parseName(end)

#print(startid)
#print(endid)

#payload = "{\n  \"avoid_systems\": [\n    30000001\n  ],\n  \"connections\": [\n    {\n      \"from\": 30000001,\n      \"to\": 30000001\n    }\n  ],\n  \"preference\": \"Shorter\",\n  \"security_penalty\": 50\n}"
#conn.request("POST", "/route/"+str(startid)+"/"+str(endid)+"", payload, headers)

#res = conn.getresponse()
#data = res.read()


#theData = json.loads(data)    


#idList = (theData['route'])
#systems = []


print(getInfo(30000240))

#for i in range(len(idList)):
#    print(idList[i])


#print(start + " to " + end + " in " + str(len(systems)) + " jumps")
#print("")
#for system in range(len(systems)):
#  print(parseID(systems[system]))