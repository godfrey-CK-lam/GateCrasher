# GateCrasher - A route analysis CLI
A simple CLI developed to analyze the hostile activity of a route between 2 systems
## Why was this developed?
This tool was developed to experiment with third-party APIs, and as such, is relatively small in scope, using 1 external API and no package imports
## How to use this tool
Simply clone the repository, navigate to the cloned directory, and then run the file, using the -h flag to understand what inputs you should be using, and that's it! No packages outside the standard library need to be installed
## Technologies
This tool only utilizes ESI (EVE Swagger Interface) for fetching information about systems, and their respective information.
This is the same information that gets displayed whenever you use the EVE Online in-game map
## Data Flow
The data flow in this project is relatively simple
1. The route (2 systems), and any additional options are recieved from the user
2. The 2 system names are transformed into system IDs with ESI to use other API methods
3. If any avoided systems are specified, these are also converted to IDs
4. The route API is called, using the system names and any additional options if present
5. The route is then calculated
6. The route is displayed in the terminal CLI
## What I learnt
As mentioned before, this was developed to experiment with working with a 3rd-party API, which I now feel comfortable doing
This was also good in learning python conventions, such as variable, function names, and general good practices
## What I would change
One change I can immediately think of, would be to also utilize the zkill API found here:
https://zkillboard.com/, this tends to return more accurate results than ESI, but is still not perfect, as ESI and zkill dont display every single killmail

If I think of any more, Ill put them here as well



