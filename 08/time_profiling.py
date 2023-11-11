import time

import classes


def create_objects(class_, n):
    objects = [class_(("team_name", 3), {1, 2, 3}) for _ in range(n)]
    return objects


def access_to_objects_attrs(objects):
    for obj in objects:
        obj.info = ("new_name", 4)
        obj.players = {4, 5, 6, 7}
        obj.add_player(9)
        obj.remove_player(4)


if __name__ == "__main__":
    N_OBJECTS = 10**6
    N_CALLS = 1

    print("\nCommon class")
    start_time = time.time()
    for i in range(N_CALLS):
        common = create_objects(classes.Team, N_OBJECTS)
    end_time = time.time()
    print(f"Creation time: {(end_time-start_time)/N_CALLS}")
    
    start_time = time.time()
    for i in range(N_CALLS):
        access_to_objects_attrs(common)
    end_time = time.time()
    print(f"Access time: {(end_time-start_time)/N_CALLS}")

    print("\nSlots class")
    start_time = time.time()
    for i in range(N_CALLS):
        slots = create_objects(classes.SlotsTeam, N_OBJECTS)
    end_time = time.time()
    print(f"Creation time: {(end_time-start_time)/N_CALLS}")

    start_time = time.time()
    for i in range(N_CALLS):
        access_to_objects_attrs(slots)
    end_time = time.time()
    print(f"Access time: {(end_time-start_time)/N_CALLS}")

    print("\nWeakref class")
    start_time = time.time()
    for i in range(N_CALLS):
        weak = create_objects(classes.WeakrefTeam, N_OBJECTS)
    end_time = time.time()
    print(f"Creation time: {(end_time-start_time)/N_CALLS}")

    start_time = time.time()
    for i in range(N_CALLS):
        access_to_objects_attrs(weak)
    end_time = time.time()
    print(f"Access time: {(end_time-start_time)/N_CALLS}")


