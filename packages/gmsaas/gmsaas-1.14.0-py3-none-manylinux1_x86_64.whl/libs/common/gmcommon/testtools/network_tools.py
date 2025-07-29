import pyspeedtest


class Location:
    FRANCE = 0
    CANADA = 1

    @staticmethod
    def to_string(location):
        if location == Location.CANADA:
            return "CANADA"
        return "FRANCE"


# http://www.speedtest.net/speedtest-servers.php
# <server url="http://{HOST}/speedtest/upload.php" ... />
HOSTS = {Location.FRANCE: "lyon3.speedtest.orange.fr", Location.CANADA: "speedtest-nl.eastlink.ca"}

INSTANCES = {}


def pretty_speed(speed):
    units = ["bps", "Kbps", "Mbps", "Gbps"]
    unit = 0
    while speed >= 1024:
        speed /= 1024
        unit += 1
    return "%0.2f %s" % (speed, units[unit])


class NetworkTest:
    def __init__(self, location):
        self._tester = pyspeedtest.SpeedTest(host=HOSTS[location], runs=5)
        self._ping = None
        self._download = None
        self._upload = None

    @property
    def ping(self):
        if self._ping is None:
            self._ping = self._tester.ping()
            print("Ping set to %d ms" % self._ping)
        return self._ping

    @property
    def download(self):
        if self._download is None:
            self._download = self._tester.download()
            print("Download set to %s" % pretty_speed(self._download))
        return self._download

    @property
    def upload(self):
        if self._upload is None:
            self._upload = self._tester.upload()
            print("Upload set to %s" % pretty_speed(self._upload))
        return self._upload


def _get_instance(location):
    if location not in INSTANCES:
        print("Creating speedtest for location %s" % location)
        INSTANCES[location] = NetworkTest(location)
    return INSTANCES[location]


def get_ping(location):
    return _get_instance(location).ping


def get_upload(location):
    return _get_instance(location).upload


def get_download(location):
    return _get_instance(location).download


def get_download_estimation_time(size_mb, location):
    speed_mbps = get_download(location) / 1024 / 1024
    return size_mb * 8 / speed_mbps


def get_upload_estimation_time(size_mb, location):
    speed_mbps = get_upload(location) / 1024 / 1024
    return size_mb * 8 / speed_mbps
