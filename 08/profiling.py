from time import time
from memory_profiler import profile

from classes import Team, SlotsTeam, WeakrefTeam
from profile_deco import ProfileDeco


@ProfileDeco
def measure_time(cls, n_instances):
    start_time = time()
    instances = [
        cls(("SomeTeam", "SPB"), {1, 2, 3})
        for _ in range(n_instances)
    ]
    print(f"Creation time of {cls.__name__} - {time()-start_time:.3f}")

    start_time = time()
    for instance in instances:
        info = instance.info
        instance.info = info
        members = instance.members
        instance.members = members
    print(f"Attr access time of {cls.__name__} - {time()-start_time:.3f}")

    return instances


@profile
def main():
    N_INSTANCES = 10**6

    team = measure_time(Team, N_INSTANCES)
    del team

    slots_team = measure_time(SlotsTeam, N_INSTANCES)
    del slots_team

    weakref_team = measure_time(WeakrefTeam, N_INSTANCES)
    del weakref_team

    measure_time.print_stat()


if __name__ == "__main__":
    main()
