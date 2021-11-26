from Consts import Consts
from requests import post, get
from threading import Lock
from pickle import dump, load
from os.path import isfile
from datetime import datetime
import Networking

mutex = Lock()


class Ingest:
    def __init__(self):
        # Loading data from file if available
        if isfile(Consts.INGEST_ID_BACKUP):
            with open(Consts.INGEST_ID_BACKUP, 'rb') as backup:
                count = load(backup)
            self.__countid = count
        else:
            self.__countid = 0

    # Sending a new scan to the PROCESS module and returning the scan id
    # While also updating the list of scans
    def add_scan(self, content):
        # Locking the count id resource
        mutex.acquire()
        self.__countid += 1

        # Backing up count id
        with open(Consts.INGEST_ID_BACKUP, 'w+b') as backup:
            dump(self.__countid, backup)
        mutex.release()

        # Send a new scan task to the PROCESS module
        # Checking availability of the service
        if Networking.check_connection('127.0.0.1', Consts.PROCESS_PORT):
            # Adding the scan to the scans list
            post("http://127.0.0.1:" + str(Consts.PROCESS_PORT) +
                 "/addtoqeue/" + str(self.__countid) + "/" + str(content) + "/" + str(datetime.now()))
            return self.__countid

        # Go a step back as a call could not be made
        mutex.acquire()
        self.__countid -= 1
        mutex.release()

        # Return failure value
        return -1

