import threading
import pyudev
from logger import Logger

Logger.set_codename('bacon')
Logger.set_module_name(__name__)
logger = Logger.get_logger()

logger.debug('Android Device Manager')
class AndroidDeviceMonitor (threading.Thread):

    def __init__(self):
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='tty')
        self.listeners = []

        threading.Thread.__init__(self)

    def run(self):
        logger.debug('Checking devices..')
        for action, device in self.monitor:
            if (action == 'add'):
                for listener in self.listeners:
                    listener.add_device(device.get('ID_SERIAL_SHORT'), device.get('ID_MODEL'), device.get('ID_FS_VERSION'))
                    # logger.debug('Device {} has been added.'
                    #     .format(device.get('ID_SERIAL_SHORT')))
            elif (action == 'remove'):
                for listener in self.listeners:
                    listener.remove_device(device.get('ID_SERIAL_SHORT'), device.get('ID_MODEL'), device.get('ID_FS_VERSION'))
                    # logger.debug('Device {} has been removed.'.format(device.get('ID_SERIAL_SHORT')))

    def add_listener(self, listener):
        self.listeners.append(listener)

if __name__ == '__main__':
    adm = AndroidDeviceMonitor()
    adm.start()
