from uiautomator import Device
import time
from logger import Logger

# Set codename and optional module_name first
Logger.set_codename('toast')
Logger.set_module_name(__name__)

# get a logger
logger = Logger.get_logger()

def customizeTo(buyer_code, device_serial):
    start_cust = time.perf_counter()

    preconfig_option = buyer_code
    logger.info("Customizing to {}".format(buyer_code))
    if buyer_code == "GLB" or "SMA":
        logger.debug("Setting buyer to preconfig option...")
        preconfig_option = buyer_code + " / single"

    logger.debug("Setting uiautomator device with {}".format(device_serial))
    print("Customizing " + str(device_serial))
    device = Device(device_serial)

    command = "service call iphonesubinfo 1 | awk -F \"'\" '{print $2}' | " \
        "sed '1 d' | tr -d '.' | awk '{print}' ORS="
    
    try:
        time.sleep(2)
        logger.debug("Getting device IMEI...")
        imei, err = device.server.adb.cmd('shell', '{}'.format(command)).communicate()
        imei = imei.decode().strip()
        logger.info("Acquired IMEI {} of device {}".format(imei, device_serial))
        key_string = '*%23272*{}'.format(imei)

        logger.debug("Dialing customization keystring...")
        device.server.adb.cmd('shell', 'am start -a android.intent.action.DIAL', 
            'tel:{}'.format(key_string)).communicate()
        logger.info("Dialed keystring {}".format(key_string))
        logger.debug("Tapping hash key...")
        device(text='#').click()
        logger.info("Hash key tapped")

        logger.debug("Searching list for the preconfig option...")
        device(className = "android.widget.ListView", resourceId = "android:id/list") \
            .child_by_text(
                preconfig_option,
                allow_scroll_search = True,
                className = "android.widget.CheckedTextView"
            ).click()
        logger.info("Preconfig option found and clicked")

        logger.debug("Tapping button matching 'INSTALL' string...")    
        device(textMatches = "INSTALL").click()
        logger.info("Button matching 'Install' found and clicked")
        time.sleep(1)
        logger.debug("Tapping option containing 'Sales' substring...")
        device(textContains = "Sales").click()
        logger.debug("Button containing 'Sales' found and clicked")
        
        logger.debug("Customization successfully completed")

        logger.debug("Intializing reboot...")
        device.server.adb.cmd('-s {} reboot'.format(device_serial))
        logger.debug("Device rebooted")

        result = {"imei": imei, "result": "Pass"}
        end_cust = time.perf_counter()
        duration = end_cust - start_cust
        logger.debug("[Pass] {} customization ended in {}s"
            .format(imei, round(duration, 2)))
        print("[Pass] {} -- {}s".format(imei, round(duration, 2)))
        return result

    except KeyboardInterrupt:
        end_cust = time.perf_counter()
        duration = end_cust - start_cust
        logger.debug("Customization manually stopped (Ctrl+C). ")
        print("All Customization stopped")
        logger.debug("[Fail] {} customization ended in {}s"
            .format(imei, round(duration, 2)))
        print("[Fail] {} -- {}s".format(imei, round(duration, 2)))
        return {"imei": imei, "result": "Fail"}

    except :
        end_cust = time.perf_counter()
        duration = end_cust - start_cust
        print("Something went wrong. Stopping device {}...".format(device_serial))
        logger.debug("[Fail] {} customization ended in {}s"
            .format(imei, round(duration, 2)))
        print("[Fail] {} -- {}s".format(imei, round(duration, 2)))
        return {"imei": imei, "result": "Fail"}


    # d(textMatches = "OK").click()
