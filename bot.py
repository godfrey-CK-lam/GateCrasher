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

DIVIDER = ("===========================================================")

# for most of these functions, it will involve:
# deconstructing the json payload into a python list
# inserting the users inputted data, into the python list
# constructing the python list back into a json payload

# to manipulate the returned values from the api calls
# the json result is loaded back into a list
# and then the data is manipulated, accordingly

# take a system name
# returns the id of the system
# or an error message, if the system doesnt exist


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
        return system + " is not a valid system"


# get a system name from the id
# returns a name of a system, corresponding to the id
def get_name(id):
    payload = '[\n  "string"\n]'
    user_payload = json.loads(payload)
    user_payload[0] = str(id)
    payload = json.dumps(user_payload, indent=2)

    CONN.request("POST", "/universe/names", payload, HEADERS)

    res = CONN.getresponse()
    data = res.read()
    return json.loads(data)[0]["name"]


# takes in a system id
# returns the name, security status, and kill count
def get_info(id):
    CONN.request("GET", "/universe/systems/" + str(id), headers=HEADERS)

    res = CONN.getresponse()
    data = res.read()
    jsonData = json.loads(data)

    return [jsonData["name"], str(round(jsonData["security_status"], 1)), str(get_kills(id))]

# helper function for get info to get the kill count of a system


def get_kills(id):
    CONN.request("GET", "/universe/system_kills", headers=HEADERS)

    res = CONN.getresponse()

    data = json.loads(res.read())

    kills = 0
    result = next((system for system in data if system["system_id"] == id), 0)

    if result:
        kills = result["pod_kills"] + result["ship_kills"]
    return kills

# find the route, based on all the user inputs


def find_route(args):
    startid = get_id(args.start)
    endid = get_id(args.end)

    payload = '{\n  "avoid_systems": [\n    30000001\n  ],\n  "connections": [\n    {\n      "from": 30000001,\n      "to": 30000001\n    }\n  ],\n  "preference": "Shorter",\n  "security_penalty": 50\n}'
    user_payload = json.loads(payload)
    user_payload["preference"] = args.preference
    user_payload["avoid_systems"] = args.avoid
    payload = json.dumps(user_payload, indent=2)

    # checking to see if any errors were present when parsing the names
    if isinstance(startid, str):
        return startid
    elif isinstance(endid, str):
        return (endid)

    CONN.request(
        "POST", "/route/" + str(startid) + "/" +
        str(endid) + "", payload, HEADERS
    )

    res = CONN.getresponse()

    data = json.loads(res.read())

    # checking if any errors were present, usually indicating a route isnt possible
    # this is usually the result of a route involving a start or end system in Pochven
    # since this tool doesnt take filaments into consideration
    if 'error' in data:
        return str("No route exists from " + args.start + " to " + args.end)

    idList = data["route"]

    route = []
    # build a list of all the system names
    for i in range(len(idList)):
        route.append(get_info(idList[i]))

    return route

# getting user arguments for use 
def get_args():

    help_text = """
    Tips: For systems with names with spaces, such as New Caldari, wrap the system in speech marks (e.g "New Caldari")
    """

    parser = argparse.ArgumentParser(
        description="Displays information about a route from one system to another", epilog=help_text
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
        help="avoid specific systems (e.g -a Bei Ongund)",
        action="store",
        nargs="+",
    )

    return parser.parse_args()

# parse user arguments, into workable data
def transform(args):

    if args.preference == "short":
        args.preference = "Shorter"
    elif args.preference == "unsafe":
        args.preference = "LessSecure"
    elif args.preference == "safe":
        args.preference = "Safer"
    else:
        # default value if no preference is listed
        args.preference = "Shorter"

    if args.avoid:
        for systems in range(len(args.avoid)):
            args.avoid[systems] = get_id(args.avoid[systems])
    else:
        # default value used by api to indicate no avoided systems
        args.avoid = [30000001]
    
    return args

# display the interface in a CLI
def display_route(route, args):

    if isinstance(route, str):
        print(DIVIDER)
        print('{:^57}'.format(*["GateCrasher - No route found"]))
        print(DIVIDER)
        print('{:^57}'.format(*[route]))
        print(DIVIDER)
        return

    print(DIVIDER)
    print('{:^57}'.format(*["GateCrasher - " + args.start +
          " to " + args.end + " in " + str(len(route)) + " jumps"]))
    print(DIVIDER)
    print('{:^19} {:^19}  {:^19}'.format(
        *['System name', 'Sec', 'Kills (last 1h)']))
    for row in route:
        print('{:^19} {:^19}  {:^19}'.format(*row))
    print(DIVIDER)
    return

# executor function
def main():
    args = get_args()
    args = transform(args)
    display_route(find_route(args), args)


if __name__ == "__main__":
    main()

# test