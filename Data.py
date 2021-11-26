from Scan import Scan
from Enums import State
from Consts import Consts
from pickle import dump, load
from os.path import isfile
from time import sleep
import json
from datetime import datetime


class Data:
    CLEAN_REFRESH_RATE_SEC = 10
    KEEP_IN_MIN = 20

    def __init__(self):
        # Loading data from file if available
        if isfile(Consts.DATASCANS_SCANS_BACKUP):
            with open(Consts.DATASCANS_SCANS_BACKUP, 'rb') as backup:
                scans = load(backup)
            self.__scans = scans
        else:
            self.__scans = {}

    # Adding a new scan to the list
    def add_scan(self, scanid, scan):
        self.__scans[scanid] = scan
        self.__update_cache()

    # Removing a scan from the list
    def remove_scan(self, scanid):
        if scanid in self.__scans:
            self.__scans.pop(scanid)

    # Changing the status of the scan based on the scan id
    def set_scan_status(self, scanid, status):
        if scanid in self.__scans:
            self.__scans[scanid].set_status(status)
            self.__update_cache()

    # Getting the status of the scan based on scan id
    def get_scan_status(self, scanid):
        if scanid in self.__scans:
            result = self.__scans[scanid].get_status()
            if result == str(State.Accepted):
                return "Accepted"
            if result == str(State.Running):
                return "Running"
            if result == str(State.Error):
                return "Error"
            if result == str(State.Complete):
                return "Completed"
        return "Not-Found"

    def clean_overdue(self):
        while True:
            if len(self.__scans) == 0:
                sleep(Data.CLEAN_REFRESH_RATE_SEC)
                continue

            templist = []
            for scanid, scan in self.__scans.items():
                now = datetime.now()
                # 2021-11-25 18:27:21.910178
                scantime = datetime.strptime(scan.get_timestamp(), "%Y-%m-%d %H:%M:%S.%f")
                delta = (now - scantime)
                seconds = delta.total_seconds()
                if seconds/60 > Data.KEEP_IN_MIN:
                    templist.append(scanid)
            for item in templist:
                self.remove_scan(item)


    # Returning all scans dictionary
    def get_all_scans(self):
        return self.__scans

    # Returning all the scan in JSON format
    def get_all_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    # Backing up current status
    def __update_cache(self):
        with open(Consts.DATASCANS_SCANS_BACKUP, 'w+b') as backup:
            dump(self.__scans, backup)

