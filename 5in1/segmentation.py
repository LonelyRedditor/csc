import numpy as np
from pprint import pprint
from random import choice
import time
from functools import total_ordering


class main_memory:
    def __init__(self, size: int = 4096):
        self.size = size
        self.job_table = []
        self.memory_map_table = {}
        self.busy_list = []
        self.free_list = []
        self.completed_list = []

    def get_status_list(self, job, status=True):
        return [i for i in job.segment_map_table if i.status == status]

    def add_job(self, name: str, size: int, location: int):
        # if not self.validate(location, size):
        # raise CustomError('This is custom error')
        curr = Job(name, size, location, self)
        self.job_table.append({"size": size, "smt location": curr.segment_map_table})
        counter = location
        curr.load_segments(self)
        ##print("ssksks")
        pprint(self.get_status_list(curr, True))
        pprint(self.get_status_list(curr, False))
        ##print("ssksks")
        self.busy_list += self.get_status_list(curr, True)
        self.free_list += self.get_status_list(curr, False)
        for i in self.job_table[-1]["smt location"]:
            if i.status:
                self.memory_map_table[counter] = i
                counter += i.size

    def validate(self, location, size):
        if not self.job_table.keys():
            return True
        loc_l = [key for key in self.job_table.keys() if key <= location][-1]
        if loc_l + self.job_table[loc_l].size > location:
            return False
        loc_u = [key for key in self.job_table.keys() if key >= location]
        if loc_u:
            return location + size > loc_u[0]
        return True  # location + size < self.size

    def check_all(self):
        for job in self.job_table:
            if any([segment.status != None for segment in job["smt location"]]):
                break
            self.job_table.remove(job)

    def show_jt(self):
        print("job table")
        for index in range(len(self.job_table)):
            pprint(self.job_table[index])
        # return "\n".join(map(str, self.job_table))

    def show_mmt(self):
        print("memory map table")
        pprint(self.memory_map_table)

    def timer(self, duration: int = 2):
        time.sleep(duration)
        self.check_all()
        victim = choice(self.busy_list)
        self.remove_segment(victim)
        self.check_all()
        self.best_fit()
        self.show_jt()
        self.show_mmt()

    def deallocate(self, index):
        # self.memory_map_table[index]
        mem = list(self.memory_map_table.keys())
        # mem.append(self.size)
        # index = segment.memory_address
        adj = [
            mem[(mem.index(index) - 1) % len(mem)],
            mem[(mem.index(index) + 1) % len(mem)],
        ]
        ##print(adj)
        # adj = self.get_adj(self.all_list, dealloc)
        ##print([i for i in adj if self.memory_map_table[i] == None])
        adj_state = [i for i in adj if self.memory_map_table[i] == None]
        # adj_state = {key: self.get_state(key) for key in adj}
        adj_state.append(index)
        adj_state.sort()
        ##print(adj, adj_state)
        self.memory_map_table[adj_state[0]] = None
        for i in adj_state[1:]:
            del self.memory_map_table[i]
        # ~ result = self.merge(new_adj)
        # ~ res0 = list(result.keys())[0]
        # ~ res1 = list(result.values())[0]
        # ~ self.free_list[res0] = res1
        # ~ self.free_list = self.sort(self.free_list)
        # ~ self.busy_list.pop(dealloc)
        # ~ print(self.free_list)
        # ~ print(self.busy_list)

    def remove_segment(self, segment):
        index = segment.memory_address
        # self.memory_map_table[index] = None
        self.deallocate(index)
        segment.complete_segment()
        self.busy_list.remove(segment)
        self.completed_list.append(segment)

    def best_fit(self):
        try:
            ##print("start")
            self.free_list.sort()
            new = min(self.free_list)
            ##print(new)
            arr = np.append(
                np.array(list(self.memory_map_table.items())), [self.size, 0]
            )
            keys = list(self.memory_map_table.keys())
            ##print(keys)
            ##print([i for i in keys if self.memory_map_table[i] == None])
            ##print(
            ##    [
            ##        np.diff(keys[keys.index(i) : keys.index(i) + 2])
            ##        for i in keys
            ##        if self.memory_map_table[i] == None
            ##    ]
            ##)
            arr = {
                i: int(np.diff(keys[keys.index(i) : keys.index(i) + 2]))
                for i in keys
                if ((self.memory_map_table[i] == None))
            }
            ##print(arr, sorted(arr.values())[-1])
            new = list(filter(lambda x: x < sorted(arr.values())[-1], self.free_list))
            ##print(new)
            # ~ if arr:
            # ~ minn = np.argmin(np.array(arr))
            # ~ print(arr[minn])
            # ~ new.status = True
            # ~ new.location = arr[minn]
            # ~ self.memory_map_table[arr[minn]] = new
            # ~ self.free_list.remove(new)
            # ~ print(self.free_list)
            if new and arr:
                minn = -1  # np.argmin(np.array(arr))
                arr = sorted(arr, key=arr.get)
                ##print(arr[-1])
                new[minn].status = True
                new[minn].memory_address = arr[minn]
                self.memory_map_table[arr[minn]] = new[minn]
                self.free_list.remove(new[minn])
                ##print(self.free_list)
            ##print("end")
        except Exception as e:
            print(e)


class Job:
    def __init__(self, name: str, size: int, location: int, mem):
        self.name = name
        self.size = size
        self.location = location
        val = (
            4
            if size < 1000
            else size // mem.size + 4
            if size > mem.size
            else size // (mem.size // 20) - 1
        )
        self.segments = np.round(
            np.round(np.random.dirichlet(np.ones(val), size=1), 1) * self.size, 0
        )
        self.segments = self.segments[self.segments != 0]
        self.segment_map_table = [
            Segment(i, j) for i, j in zip(range(len(self.segments)), self.segments)
        ]

    def load_segments(self, memory):
        index = self.location
        for i in self.segment_map_table:
            if self.validate(i, memory, index):
                i.status = True
                i.memory_address = index
                memory.memory_map_table[index] = i
                index += i.size

    def validate(self, segment, memory, index=0):
        ##print("vall", index, segment.size, index + segment.size, memory.size)
        return index + segment.size < memory.size

    def show_smt(self):
        return "\n".join(map(str, self.segment_map_table))

    def __repr__(self):
        return f"{self.name} ({self.size})"


@total_ordering
class Segment:
    def __init__(
        self, number: int, size: int, status: bool = False, memory_address: int = None
    ):
        self.number = number
        self.size = size
        self.status = status
        self.memory_address = memory_address

    def complete_segment(self):
        self.status = None
        self.memory_address = None

    def __lt__(self, other):
        if type(other) == int:
            return self.size < other
        return self.size < other.size

    def __repr__(self):
        return f"segment {self.number} | ({self.status}) | {self.size} | {self.memory_address}"


class Memory_manager:
    def __init__(self, size):
        self.size = size
        mem = main_memory(size)
        self.mem = mem
        mem.add_job("vlc", 900, 1500)
        mem.add_job("chrome", 1200, 2400)
        mem.add_job("spotify", 1000, 3600)
        mem.add_job("terminal", 700, 3700)
        mem.show_jt()
        mem.show_mmt()
        ##print("======busy==========" * 30)
        pprint(mem.busy_list)
        ##print("=======free=========" * 30)
        pprint(mem.free_list)
        while mem.free_list and mem.busy_list:
            mem.timer()

memory_man = Memory_manager(4096)
