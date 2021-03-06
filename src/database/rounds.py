from database.games import Game
from utils import groups


class Round(object):
    def __init__(self, idx, gamers, games=None, group_size=4):
        """
        :param idx: The round index
        :param gamers: a list of all the participant user IDs
        :param games: a list of Game objects
        :param group_size: maximum size of created groups
        :param round_complete: is round complete?
        """
        self.idx = idx
        self.gamers = gamers
        self.games = games
        self.groupSize = group_size

        if self.games is None:
            self.games = []
            for idx, group in enumerate(groups.make_groups(self.gamers, self.groupSize)):
                self.games.append(
                    Game(
                        idx=idx,
                        gamers=group
                    )
                )

    @staticmethod
    def from_dict(source):
        round = Round(idx=source['idx'], games=[Game.from_dict(game) for game in source['games']], gamers=source['gamers'], group_size=source['group_size'])

        return round

    def to_dict(self):
        dest = {
            'idx': self.idx,
            'games': [game.to_dict() for game in self.games],
            'gamers': self.gamers,
            'group_size': self.groupSize
        }
        return dest

    def round_complete(self):
        return all(game.winner is not None for game in self.games)

    def generate_status_message(self):
        out = ''
        if self.round_complete():
            if len(self.games) > 1:
                out += f'Round {self.idx} complete! Please congratulate the following players:'
                for game in self.games:
                    out += f'\n <@{game.winner}> for winning game {game.idx}'
            elif len(self.games) == 1:
                out += f'Congratulations, <@{self.games[0].winner}> for winning the gaming tournament!'
            else:
                out += f'No games running'
        else:
            out += f'Round {self.idx} in progress... please wait for games to be completed'
            for game in self.games:
                out += f'\nGame {game.idx} - '
                if game.winner:
                    out += f'won by <@{game.winner}>'
                else:
                    out += 'in progress'
        return out[:1999]

    def winners(self):
        if self.round_complete():
            return [game.winner for game in self.games]
        else:
            return False

    def game_from_channel_id(self, id):
        return next((g for g in self.games if g.tc_id == id), False)
