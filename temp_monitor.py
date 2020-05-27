import os
import time
from logger import Logger

# Set codename and optional module_name first
Logger.set_codename('toast')
Logger.set_module_name(__name__)

# get a logger
logger = Logger.get_logger()

def measure_temp():
        temp = os.popen("vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'").readline()
        return float(temp)

def start_temperature_check():
        while True:
                temperature = measure_temp()
                if temperature >= 80:
                        print(temperature) 
                        logger.warning("Temperature: {}".format(temperature))
                elif temperature >= 70:
                        print(temperature) 
                        logger.info("Temperature: {}".format(temperature))
                elif temperature >= 60:
                        print(temperature) 
                        logger.info("Temperature: {}".format(temperature))
                elif temperature >= 50:
                        print(temperature) 
                        logger.info("Temperature: {}".format(temperature))
                elif temperature >= 40:
                        print(temperature) 
                        logger.info("Temperature: {}".format(temperature))
                

                time.sleep(1)