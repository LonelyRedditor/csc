from copy import deepcopy
from threading import RLock

class MonitorVehicleTracker:
    def __init__(self, locations: dict[str, dict[str, int]]):
        self._lock = RLock()
        self._locations = locations

    def getLocations(self) -> dict[str, dict[str, int]]:
        with self._lock:
            self._lock.acquire()
            return deepcopy(self._locations)

    def getLocation(self, id:str) -> dict[str, int]:
        with self._lock:
            self._lock.acquire()
            return deepcopy(self._locations[id])


    def setLocation(self, id:str, long:int, lat:int):
        with self._lock:
            loc = self._locations[id]
            loc["long"] = long
            loc["lat"] = lat

if __name__ == "__main__":
    locations = {"a": {"long": 1, "lat": 2}, "b": {"long": 3, "lat": 4}}
    tracker = MonitorVehicleTracker(locations)
    print(tracker.getLocations())
    print(tracker.getLocation("a"))
    tracker.setLocation("a", 10, 20)
    print(tracker.getLocations())