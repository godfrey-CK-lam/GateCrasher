import argparse
import http.client
import json

parser = argparse.ArgumentParser()
parser.add_argument('start', type=str)
parser.add_argument('end', type=str)
args = parser.parse_args()

start = '\"' + args.start + '\"'
end = '\"' + args.end + '\"'



def parseName(system):
    conn = http.client.HTTPSConnection("esi.evetech.net")
    payload = "[\n" + system + "\n]"

    headers = {
        'Accept-Language': "en",
        'If-None-Match': "",
        'X-Compatibility-Date': "2025-11-06",
        'X-Tenant': "",
        'Content-Type': "application/json",
        'Accept': "application/json"
    }

    conn.request("POST", "/universe/ids", payload, headers)

    res = conn.getresponse()
    allData = res.read()
    parseData = json.loads(allData)    

    data = parseData.get("systems",[])
    print(data[0]["id"])

   #test
  
    
parseName(start)
parseName(end)



