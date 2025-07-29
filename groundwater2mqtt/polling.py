import requests
from bs4 import BeautifulSoup
import asyncio
import logging
import aiomqtt

async def task(procdata):
    logging.debug("Starting scraper process")
    while 1:
        try:
            async with aiomqtt.Client(
                                    hostname = procdata["server"],
                                    port = procdata["port"],
                                    username = procdata["user"],
                                    password = procdata["password"],
                                    ) as client:  
                while 1:
                    logging.debug("Scraping")
                    response = requests.get(procdata["url"])
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        tables = soup.find_all('table')
                        rows = []
                        for row in tables[0].tbody.find_all('tr'):    
                            # Find all data for each column
                            columns = row.find_all('td')
                            
                            if(len(columns) == 3):
                                datum = columns[0].text.strip()
                                levelNN = columns[1].text.strip()
                                levelAbs = columns[2].text.strip()
                                rows += [(datum,levelNN,levelAbs)]
                        if len(rows) > 0:
                            _,level,_ = rows[0]
                            level = level.replace(",",".")
                            flevel = float(level)
                            pf = procdata["prefix"]
                            id = procdata["id"]
                            logging.info("Publishing: {} - {}".format(pf + id + "/level",flevel))
                            await client.publish(pf + id + "/level",payload="{}".format(flevel))
                        else:
                            logging.error("Not enough rows found in HTML table.")  
                    else:
                        logging.error("Status code {} returned by web server".format(response.status_code))  
                    await asyncio.sleep(1000.0) 
        except aiomqtt.MqttError:
            logging.ERROR(f"Connection lost; Reconnecting in 3 seconds ...")
            await asyncio.sleep(3)
