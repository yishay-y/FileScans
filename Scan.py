class Scan:

    def __init__(self, scanid, content, status, timestamp):
        self.__scanid = scanid
        self.__content = content
        self.__status = status
        self.__timestamp = timestamp

    def get_scan_id(self):
        return self.__scanid

    def get_content(self):
        return self.__content

    def get_status(self):
        return self.__status

    def get_timestamp(self):
        return self.__timestamp

    def set_status(self, status):
        self.__status = status
