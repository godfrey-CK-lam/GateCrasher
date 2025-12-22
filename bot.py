import argparse
import http.client
import json
import datetime

# parse a system name to the id
def getID(system):
    
    payload =  "[\n  \"string\"\n]"
    myPayload = json.loads(payload)
    myPayload[0] = system
    payload = json.dumps(myPayload, indent=2)
   
    conn.request("POST", "/universe/ids", payload, headers)

    res = conn.getresponse()
    allData = res.read()
    parseData = json.loads(allData)    

    data = parseData.get("systems")
    return data[0]["id"]

  
# parse a system ID to a name
def getName(id):
    payload =  "[\n  \"string\"\n]"
    myPayload = json.loads(payload)
    myPayload[0] = str(id)
    payload = json.dumps(myPayload, indent=2)

    conn.request("POST", "/universe/names", payload, headers)

    res = conn.getresponse()
    data = res.read()
    jsonData = json.loads(data)    
    return jsonData[0]['name']

def getInfo(id):
    conn.request("GET", "/universe/systems/" + str(id), headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    jsonData = json.loads(data)   
    
    return [jsonData['name'], round(jsonData['security_status'], 1), getKills(id)]

def getKills(id):
    conn.request("GET", "/universe/system_kills", headers=headers)

    res = conn.getresponse()
    data = res.read()
    parseData = json.loads(data)  

    kills = 0
    result = next((obj for obj in parseData if obj["system_id"] == id),0) 
    
    if result:
        kills = result["pod_kills"] + result["ship_kills"]
    return kills

def findRoute(start, end, preference, avoid):
    startid = getID(start)
    endid = getID(end)


    payload = "{\n  \"avoid_systems\": [\n    30000001\n  ],\n  \"connections\": [\n    {\n      \"from\": 30000001,\n      \"to\": 30000001\n    }\n  ],\n  \"preference\": \"Shorter\",\n  \"security_penalty\": 50\n}"
    myPayload = json.loads(payload)
    myPayload['preference'] = preference
    myPayload['avoid_systems'] = avoidSystems
    payload = json.dumps(myPayload, indent=2)
    
    conn.request("POST", "/route/"+str(startid)+"/"+str(endid)+"", payload, headers)

    res = conn.getresponse()
    data = res.read()
    theData = json.loads(data)    
 
    idList = (theData['route'])
    route = []

    for i in range(len(idList)):
        route.append(getInfo(idList[i]))

    return route


conn = http.client.HTTPSConnection("esi.evetech.net")

headers = {
        'Accept-Language': "en",
        'If-None-Match': "",
        'X-Compatibility-Date': "2025-12-16", #time.strftime("%Y-%m-%d")
        'X-Tenant': "",
        'Content-Type': "application/json",
        'Accept': "application/json"
    }


parser = argparse.ArgumentParser(description="Displays information about a route from one system to another")
parser.add_argument('start', type=str,help=("The starting system"))
parser.add_argument('end', type=str, help="The destination system")
parser.add_argument('-p', '--preference', help="Route preferences", choices=["short","unsafe","safe"])
parser.add_argument('-a', '--avoid', type=str, help="avoid specific systems", action='store', nargs="+")

args = parser.parse_args()

avoidSystems = []

if args.preference == "short":
    preference = "Shorter"
elif args.preference =="unsafe":
    preference = "LessSecure"
elif args.preference =="safe":
    preference = "Safer"
else:
    preference = "Shorter"

if args.avoid:
    for systems in range(len(args.avoid)):
        avoidSystems.append(getID(args.avoid[systems]))
else:
    avoidSystems = [30000001]


conn = http.client.HTTPSConnection("esi.evetech.net")

headers = {
        'Accept-Language': "en",
        'If-None-Match': "",
        'X-Compatibility-Date': "2025-12-16", #time.strftime("%Y-%m-%d")
        'X-Tenant': "",
        'Content-Type': "application/json",
        'Accept': "application/json"
    }

print(findRoute(args.start, args.end, preference, avoidSystems))