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
    if buyer_code == "GLB" or "SMA":
        preconfig_option = buyer_code + " / single"

    print("Customizing " + str(device_serial))
    command = "service call iphonesubinfo 1 | awk -F \"'\" '{print $2}' | sed '1 d' | tr -d '.' | awk '{print}' ORS="
    device = Device(device_serial)
    
    try:
        time.sleep(2)
        imei, err = device.server.adb.cmd('shell', '{}'.format(command)).communicate()
        imei = imei.decode().strip()
        key_string = '*%23272*{}'.format(imei)

        device.server.adb.cmd('shell', 'am start -a android.intent.action.DIAL', 
            'tel:{}'.format(key_string)).communicate()
        device(text='#').click()
    
        device(className = "android.widget.ListView", resourceId = "android:id/list") \
            .child_by_text(
                preconfig_option,
                allow_scroll_search = True,
                className = "android.widget.CheckedTextView"
            ).click()
            
        device(textMatches = "INSTALL").click()
        time.sleep(1)
        device(textContains = "Sales").click()
        result = {"imei": imei, "result": "Pass"}
        device.server.adb.cmd('-s {} reboot'.format(device_serial))
        end_cust = time.perf_counter()
        duration = end_cust - start_cust
        print("[Pass] {} -- {}s".format(imei, round(duration, 2)))
        return result

    except KeyboardInterrupt:
        end_cust = time.perf_counter()
        duration = end_cust - start_cust
        print("Customization stopped.")
        print("[Fail] {} -- {}s".format(imei, round(duration, 2)))
        return {"imei": imei, "result": "Fail"}

    except:
        end_cust = time.perf_counter()
        duration = end_cust - start_cust
        print("Something went wrong. Stopping device {}...".format(device_serial))
        print("[Fail] {} -- {}s".format(imei, round(duration, 2)))
        return {"imei": imei, "result": "Fail"}


    # d(textMatches = "OK").click()
