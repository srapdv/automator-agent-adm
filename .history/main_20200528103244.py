# code_name: toast
# name: Simoun Raphael de Vera
# description: Automator agent module
# version: 1.0


from logger import Logger
from uiautomator import Device
import adm
import adl
import customizer
import threading
import time
import sys
# import temp_monitor


Logger.set_codename('toast')
Logger.set_module_name(__name__)
logger = Logger.get_logger()
device_list = []
results = {}
runningThreads = []
start = 0
end = 0

class AndroidAgentDeviceListener(adl.AndroidDeviceListener): 
    def _init_(self):
        pass
    
    def add_device(self, serial_number, model, os_version):
        logger.debug('Device {} has been added.'
            .format(serial_number))
        
        device_list.append(serial_number)
        for device in device_list:
            time.sleep(2)
            customizerThread = customizationThread(device)
            logger.debug("Setting device {} to {} thread"
                .format(device, customizerThread.name))
            logger.debug("Checking if {} thread already exists..."
                .format(customizerThread.name))
            if customizerThread.checkIfRunning(customizerThread):
                logger.debug("{} thread already exists. Passing..."
                .format(customizerThread.name))
                pass
            else:
                logger.debug("Creating {} thread..."
                    .format(customizerThread.name))
                customizerThread.start()

                # A try/catch statement that checks if the device already has a "Passed"
                # result.
                # 
                # try:
                #     if results[device]["result"] != "Pass":
                #         logger.debug("Retrying to run device {}..."
                #             .format(device))
                #         customizerThread.start()
                # except:
                #     logger.debug("Starting {} thread..."
                #         .format(customizerThread.name))
                #     customizerThread.start()
            
    def remove_device(self, serial_number, model, os_version):
        try:
            device_list.remove(serial_number)
            runningThreads.remove(serial_number)
            logger.info("Device {} disconnected"
                .format(serial_number))
            # start = time.perf_counter()
            # print('Start: ' + str(start))
        except:
            pass        
        # print(str(device_list))   


class customizationThread(threading.Thread):
    def __init__(self, device_serial):
        threading.Thread.__init__(self)
        self.device_serial = device_serial
        self.name = device_serial

    def run(self):
        logger.info("Starting customization on device {}".format(self.device_serial))
        results[self.device_serial] = customizer.customizeTo(
            sys.argv[1].upper(), self.device_serial)
        # print(results)

    def checkIfRunning(self, newThread):
        if newThread.name in runningThreads: 
            logger.debug("Thread {} already up and running.".format(newThread.name))
            return True
        else:
            runningThreads.append(newThread.name)
    

if __name__ == "__main__":
    # temp_monitor.start_temperature_check()
    logger.info("Starting to listen for devices...")
    listener = AndroidAgentDeviceListener()
    adm = adm.AndroidDeviceMonitor()

    adm.add_listener(listener)
    try:
        adm.start()
    except KeyboardInterrupt:
        print('Exiting...')
        logger.info('Close command initialized. Script closed.')
        sys.exit()
    except:
        print('Something went wrong')
        logger.info('Something went wrong. Script closed.')
        sys.exit()