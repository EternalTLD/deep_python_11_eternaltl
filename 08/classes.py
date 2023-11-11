import weakref


class TeamInfo:
    def __init__(self, name, players_number) -> None:
        self.name = name
        self.players_number = players_number


class Players:
    def __init__(self, players) -> None:
        self.players = players


class Team:
    def __init__(self, info, players) -> None:
        self.info = TeamInfo(*info)
        self.players = Players(players)

    def add_player(self, player):
        self.players.add(player)
    
    def remove_player(self, player):
        self.players.remove(player)


class SlotsTeamInfo:
    __slots__ = ("name", "players_number")

    def __init__(self, name, players_number) -> None:
        self.name = name
        self.players_number = players_number


class SlotsPlayers:
    __slots__ = ("players")

    def __init__(self, players) -> None:
        self.players = players


class SlotsTeam:
    __slots__ = ("info", "players")

    def __init__(self, info, players) -> None:
        self.info = SlotsTeamInfo(*info)
        self.players = SlotsPlayers(players)

    def add_player(self, player):
        self.players.add(player)
    
    def remove_player(self, player):
        self.players.remove(player)


class WeakrefTeam:
    def __init__(self, info, players) -> None:
        self.info = weakref.ref(TeamInfo(*info))
        self.players = weakref.ref(Players(players))
    
    def add_player(self, player):
        self.players.add(player)
    
    def remove_player(self, player):
        self.players.remove(player)
