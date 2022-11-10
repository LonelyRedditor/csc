import numpy as np


def bankers_algorithm(
    alloc: np.ndarray, max_mat: np.ndarray, avail: np.ndarray
) -> list:
    """
    Allocation Matrix {alloc}
    Max Matrix {max_mat}
    Available resources {avail}
    """
    needs = max_mat - alloc
    needs_ = max_mat - alloc
    finished = [not any(i) for i in needs]
    prev_avail = finished
    while not all(finished):
        prev_avail = avail.copy()
        for process in needs:
            safe = all(process <= avail)
            status = ["032", "accepted"] if safe else ["31", "rejected"]
            loc = np.argwhere((needs_ == process).all(axis=1))[0][0]
            print(f"\033[{status[0]};1mP{loc}", process, f"{status[1]}\033[0m")
            if not safe:
                print("")
                continue
            avail += alloc[loc]
            print(f"\033[032;1mAvailable memory => {avail} \033[0m\n")
            loc = np.argwhere((needs == process).all(axis=1))[0][0]
            needs = np.delete(needs, loc, axis=0)
            finished = [not any(i) for i in needs]
        if np.array_equal(prev_avail, avail, equal_nan=True):
            return f"\nDeadlock at {needs}\n Available memory => {avail}\n"
    return "No deadlock, tasks completed"


alloc = np.array([[0, 1, 0], [2, 1, 0], [3, 0, 2], [2, 1, 1], [1, 0, 2]])
max_mat = np.array([[7, 5, 3], [3, 4, 2], [12, 0, 2], [2, 1, 2], [5, 3, 3]])
avail = np.array([3, 3, 2])
print(bankers_algorithm(alloc, max_mat, avail))

print("\n\n")

alloc = np.array([[2, 0, 1, 1], [0, 1, 2, 1], [4, 0, 0, 3], [0, 2, 1, 0], [1, 0, 3, 0]])
max_mat = np.array(
    [[3, 2, 1, 4], [43, 2, 5, 2], [5, 1, 0, 5], [1, 5, 3, 0], [3, 0, 3, 3]]
)
avail = np.array([1, 2, 2, 2])
print(bankers_algorithm(alloc, max_mat, avail))
