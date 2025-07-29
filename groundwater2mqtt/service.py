import json
import asyncio
import logging

import polling
import discovery

logging.getLogger("root").setLevel(logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARN)

# Open and read the JSON file
with open('data/options.json', 'r') as file:
    data = json.load(file)

procdata = { 
        "url": data["url"],
        "id": data["id"],
        "prefix": data["mqtt_prefix"],
        "server": data["mqtt_server"],
        "port": data["mqtt_port"],
        "user": data["mqtt_user"],
        "password": data["mqtt_password"],
    }

async def main():
    await asyncio.gather(
        polling.task(procdata),
        discovery.task(procdata)
    )

asyncio.run(main())