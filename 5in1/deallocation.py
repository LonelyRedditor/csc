class dynamic_partition_system:
    def __init__(self, free_list: dict, busy_list: dict):
        self.free_list = free_list
        self.busy_list = busy_list
        # self.all_list = busy_list | free_list # python3.9+
        self.all_list = self.sort({**busy_list, **free_list})

    def get_index(self, dict_, value):
        return list(dict_.keys()).index(value)

    def get_adj(self, dict_, value):
        index = self.get_index(dict_, value)
        keys = list(dict_.keys())
        res = []
        if index <= len(dict_) - 1:
            res.append(keys[index - 1])
        if index >= 0:
            res.append(keys[index + 1])
        return res

    def get_state(self, key):
        try:
            busy = self.busy_list[key]
            return "busy"
        except:
            free = self.free_list[key]
            return "free"

    def filter_(self, dict_, value="free"):
        return dict((i, j) for i, j in dict_.items() if j == value)

    def sort(self, dict_, key=0):
        return dict(sorted(dict_.items(), key=lambda x: x[key]))

    def merge(self, dict_):
        print(dict_.items())
        return {list(dict_.keys())[0]: sum(list(dict_.values()))}

    def deallocate(self, dealloc):
        index = self.get_index(self.all_list, dealloc)
        adj = self.get_adj(self.all_list, dealloc)
        adj_state = {key: self.get_state(key) for key in adj}
        new_adj = self.sort(
            {
                **{i: self.free_list[i] for i in self.filter_(adj_state)},
                **{dealloc: self.busy_list[dealloc]},
            }
        )
        result = self.merge(new_adj)
        res0 = list(result.keys())[0]
        res1 = list(result.values())[0]
        self.free_list[res0] = res1
        self.free_list = self.sort(self.free_list)
        self.busy_list.pop(dealloc)
        print(self.free_list)
        print(self.busy_list)


free_list = {
    4075: 105,
    5225: 5,
    6785: 600,
    7560: 20,
    7800: 5,
    10250: 4050,
    15125: 230,
    24500: 1000,
}

busy_list = {7580: 20, 7600: 200, 7805: 1000, 8805: 445, 9250: 1000}

system = dynamic_partition_system(free_list, busy_list)
dealloc = 7600
system.deallocate(dealloc)
