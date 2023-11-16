import weakref


class TeamInfo:
    def __init__(self, name, city) -> None:
        self.name = name
        self.city = city


class Members:
    def __init__(self, members) -> None:
        self.members = members


class Team:
    def __init__(self, info, members) -> None:
        self.info = TeamInfo(*info)
        self.members = Members(members)


class SlotsTeam:
    __slots__ = ("info", "members")

    def __init__(self, info, members) -> None:
        self.info = TeamInfo(*info)
        self.members = Members(members)


class WeakrefTeam:
    def __init__(self, info, members) -> None:
        self.info = weakref.ref(TeamInfo(*info))
        self.members = weakref.ref(Members(members))
