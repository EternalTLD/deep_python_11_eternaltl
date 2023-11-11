import time
from memory_profiler import profile

from classes import Team, SlotsTeam, WeakrefTeam
from profile_deco import ProfileDeco


@ProfileDeco
def measure_time(cls, n_instances, n_calls):
    start_time = time.time()
    for _ in range(n_calls):
        instances = [
            cls(("SomeTeam", "SPB"), {1, 2, 3}, "Active", "Volleyball")
            for _ in range(n_instances)
        ]
    print(f"Creation time of {cls.__name__} - {(time.time()-start_time)/n_calls}")

    start_time = time.time()
    for _ in range(n_calls):
        for inst in instances:
            inst.info = ("Team", "MSK")
            inst.members = {4, 5, 6, 7}
            inst.status = "Inactive"
            inst.sport = "Soccer"
    print(f"Attr access time of {cls.__name__} - {(time.time()-start_time)/n_calls}")

    return instances


@profile
def main():
    N_OBJECTS = 5 * 10**5
    N_CALLS = 5

    team = measure_time(Team, N_OBJECTS, N_CALLS)
    del team
    slots_team = measure_time(SlotsTeam, N_OBJECTS, N_CALLS)
    del slots_team
    weakref_team = measure_time(WeakrefTeam, N_OBJECTS, N_CALLS)
    del weakref_team

    measure_time.print_stat()


if __name__ == "__main__":
    main()
