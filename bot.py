import argparse
import http.client
import json

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
        'X-Compatibility-Date': "2025-11-06",
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
    alldata = res.read()
    parseData = json.loads(alldata)    
    return parseData[0]['name']
        


#print(start)
startid = parseName(start)
endid = parseName(end)

#print(startid)
#print(endid)

payload = "{\n  \"avoid_systems\": [\n    30000001\n  ],\n  \"connections\": [\n    {\n      \"from\": 30000001,\n      \"to\": 30000001\n    }\n  ],\n  \"preference\": \"Shorter\",\n  \"security_penalty\": 50\n}"
conn.request("POST", "/route/"+str(startid)+"/"+str(endid)+"", payload, headers)

res = conn.getresponse()
data = res.read()


parseData = json.loads(data)    
systems = (parseData['route'])

print()
for system in range(len(systems)):
  print(parseID(systems[system]))