import argparse
import http.client
import json
import datetime

CONN = http.client.HTTPSConnection("esi.evetech.net")

HEADERS = {
    "Accept-Language": "en",
    "If-None-Match": "",
    "X-Compatibility-Date": "2025-12-16",  # time.strftime("%Y-%m-%d")
    "X-Tenant": "",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

DIVIDER = ("======================================================")

# parse a system name to the id


def get_id(system):

    payload = '[\n  "string"\n]'
    user_payload = json.loads(payload)
    user_payload[0] = system
    payload = json.dumps(user_payload, indent=2)

    CONN.request("POST", "/universe/ids", payload, HEADERS)

    res = CONN.getresponse()

    data = json.loads(res.read())
    actual = data.get("systems")
    try:
        return actual[0]["id"]
    except:
        print(system + " is an invalid system name (please check the spelling!)")
        exit(1)


# parse a system ID to a name
def get_name(id):
    payload = '[\n  "string"\n]'
    user_payload = json.loads(payload)
    user_payload[0] = str(id)
    payload = json.dumps(user_payload, indent=2)

    CONN.request("POST", "/universe/names", payload, HEADERS)

    res = CONN.getresponse()
    data = res.read()
    return json.loads(data)[0]["name"]


def get_info(id):
    CONN.request("GET", "/universe/systems/" + str(id), headers=HEADERS)

    res = CONN.getresponse()
    data = res.read()
    jsonData = json.loads(data)

    return [jsonData["name"], str(round(jsonData["security_status"], 1)), str(get_kills(id))]


def get_kills(id):
    CONN.request("GET", "/universe/system_kills", headers=HEADERS)

    res = CONN.getresponse()

    data = json.loads(res.read())

    kills = 0
    result = next((system for system in data if system["system_id"] == id), 0)

    if result:
        kills = result["pod_kills"] + result["ship_kills"]
    return kills


def find_route(args):
    startid = get_id(args.start)
    endid = get_id(args.end)

    payload = '{\n  "avoid_systems": [\n    30000001\n  ],\n  "connections": [\n    {\n      "from": 30000001,\n      "to": 30000001\n    }\n  ],\n  "preference": "Shorter",\n  "security_penalty": 50\n}'
    user_payload = json.loads(payload)
    user_payload["preference"] = args.preference
    user_payload["avoid_systems"] = args.avoid
    payload = json.dumps(user_payload, indent=2)

    CONN.request(
        "POST", "/route/" + str(startid) + "/" +
        str(endid) + "", payload, HEADERS
    )

    res = CONN.getresponse()

    data = json.loads(res.read())
    idList = data["route"]
    route = []

    for i in range(len(idList)):
        route.append(get_info(idList[i]))

    return route


def get_args():

 

    parser = argparse.ArgumentParser(
        description="Displays information about a route from one system to another", epilog="HELP"
    )
    parser.add_argument("start", type=str, help=("The starting system"))
    parser.add_argument("end", type=str, help="The destination system")
    parser.add_argument(
        "-p",
        "--preference",
        help="Route preferences",
        choices=["short", "unsafe", "safe"],
    )
    parser.add_argument(
        "-a",
        "--avoid",
        type=str,
        help="avoid specific systems",
        action="store",
        nargs="+",
    )

    return parser.parse_args()


def transform(args):

    # print(vars(args))

    if args.preference == "short":
        args.preference = "Shorter"
    elif args.preference == "unsafe":
        args.preference = "LessSecure"
    elif args.preference == "safe":
        args.preference = "Safer"
    else:
        args.preference = "Shorter"

    if args.avoid:
        for systems in range(len(args.avoid)):
            args.avoid[systems] = get_id(args.avoid[systems])
    else:
        args.avoid = [30000001]

    # print(vars(args))
    return args

def display(route, args):

    print(DIVIDER)
    print('{:^52}'.format(*['GateCrasher - Results']))
    print(DIVIDER)
    print('{:^52}'.format(*[args.start + " to " + args.end + " in " + str(len(route)) + " jumps"]))
    print(DIVIDER)
    print('{:^18} {:^18}  {:^18}'.format(*['System name', 'Sec', 'Kills']))
    for row in route:
        print('{:^18} {:^18}  {:^18}'.format(*row))
    print(DIVIDER)
    return


def main():

    args = get_args()
    args = transform(args)


    display(find_route(args), args)


if __name__ == "__main__":
    main()
