import asyncio
import logging
import aiomqtt
import json

async def task(procdata):
    prefix = procdata["prefix"]
    id = procdata["id"]

    while 1:
        logging.debug("Discovering")
        logging.info("[{}] publishing HA discovery".format(id))

        sensor_dict = {
            "device": {
                "identifiers": ["groundwater_{}".format(id.replace("-","_"))],
                "name": "Groundwater {}".format(id),
                "manufacturer": "Web Scraper",
            },
            "origin": {
                "name": "Groundwater2MQTT"
            },
            "qos": 1,
            "name": "Level",
            "unique_id": id + "_level",
            "state_topic": prefix + id + "/level",
            "unit_of_measurement": "m",
        }
        async with aiomqtt.Client(
                hostname = procdata["server"],
                port = procdata["port"],
                username = procdata["user"],
                password = procdata["password"],
                clean_session=True
                ) as client:  
            await client.publish("homeassistant/sensor/{}/config".format(id + "_level"),payload="{}".format(json.dumps(sensor_dict)),qos=1,retain=True)

        await asyncio.sleep(750)
