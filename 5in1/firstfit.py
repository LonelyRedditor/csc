class MemoryAllocation:
    def __init__(self, requested, locations):
        self.requested = requested
        self.locations = locations

    def first_fit_allocation(self):
        requested = self.requested.copy()
        locations = self.locations.copy()
        print("\n======================")
        print("FIRST FIT ALLOCATION")
        print("======================")
        print("Memory    | Memory\nrequested | block size")
        for i in range(len(requested)):
            for j in range(len(locations)):
                request = requested[i]
                location = locations[j]
                if request <= location:
                    print(request, " " * 8, location)
                    locations.remove(location)
                    break
        print("\n")


locations = [15, 100, 70, 20, 50]
requested = [10, 20, 30, 10, 60, 30, 50, 300, 700]
test_example = MemoryAllocation(requested, locations)
test_example.first_fit_allocation()
