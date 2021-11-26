import random
from Enums import State
from time import sleep
from Consts import Consts
from requests import post
from pickle import dump, load
from os.path import isfile
from Scan import Scan
import Networking


class Process:
    SCAN_MIN_TIME = 1
    SCAN_MAX_TIME = 10
    SCAN_STEP = 1
    REFRESH_RATE = 2

    def __init__(self):
        # Loading the pending scans queue if available
        if isfile(Consts.PROCESS_QUEUE_BACKUP):
            with open(Consts.PROCESS_QUEUE_BACKUP, 'rb') as backup:
                queue = load(backup)
            self.__scan_ids_queue = queue
        else:
            self.__scan_ids_queue = []

        # Loading the completed scans list of available
        # The purpose of holding this list is to keep track of completed scan in case of a crash
        if isfile(Consts.PROCESS_DONE_BACKUP):
            with open(Consts.PROCESS_DONE_BACKUP, 'rb') as backup:
                done = load(backup)
            self.__done = done
        else:
            self.__done = []

    # Adding the scan to the pending scans
    def add_scan_to_queue(self, scan):
        self.__scan_ids_queue.append(scan)
        self.__update_cache()
        if Networking.check_connection('127.0.0.1', Consts.DATA_PORT):
            post("http://127.0.0.1:" + str(Consts.DATA_PORT) +
                 "/addscan/" + str(scan.get_scan_id()) + "/" +
                 str(scan.get_content()) + "/" + str(scan.get_timestamp()))

    # Performing a single scan for the respective scan id
    def __initiate_scan(self, scan):
        # Checking availability of the service
        if Networking.check_connection('127.0.0.1', Consts.DATA_PORT):
            post("http://127.0.0.1:" + str(Consts.DATA_PORT) +
                 "/setstatus/" + str(scan.get_scan_id()) + "/" + str(State.Running))

        # Simulate scanning by generating random running time and random result
        time = random.randrange(Process.SCAN_MIN_TIME, Process.SCAN_MAX_TIME, Process.SCAN_STEP)
        result = random.randrange(0, 2, 1)
        if result == 0:
            result = State.Error
        else:
            result = State.Complete
        sleep(time)

        # Updating the status and moving to complete queue
        scan.set_status(result)
        self.__done.append(scan)
        self.__update_cache()

    # Main method to start performing scans one by one
    def scan_all(self):
        print("Started listening")
        while True:
            if len(self.__scan_ids_queue) == 0:
                sleep(Process.REFRESH_RATE)
                continue
            else:
                scan = self.__scan_ids_queue.pop()
                self.__initiate_scan(scan)

    # Clearing completed scans after documenting the result of the scan
    def update_done(self):
        print("Cleaning done queue")
        while True:
            if len(self.__done) == 0:
                sleep(Process.REFRESH_RATE)
                continue
            else:
                # Checking availability of the service
                if Networking.check_connection('127.0.0.1', Consts.DATA_PORT):
                    scan = self.__done.pop()
                    post("http://127.0.0.1:" + str(Consts.DATA_PORT) +
                         "/updatescan/" + str(scan.get_scan_id()) + "/" + str(scan.get_status()) + "/" +
                         str(scan.get_status()) + "/" + str(scan.get_timestamp()))

    # Backing up the lists
    def __update_cache(self):
        with open(Consts.PROCESS_QUEUE_BACKUP, 'w+b') as backup:
            dump(self.__scan_ids_queue, backup)
        with open(Consts.PROCESS_DONE_BACKUP, 'w+b') as backup:
            dump(self.__done, backup)


class ScanStatus:
    def __init__(self, scanid, status):
        self.__scanid = scanid
        self.__status = status

    def get_scan_id(self):
        return self.__scanid

    def get_scan_status(self):
        return self.__status

    def set_scan_status(self, status):
        self.__status = status
