games = {}


class Game:
    def __init__(self, game_id) -> None:
        self.game_id = game_id
        self.state = 'drawing'

    def update_canvas(self, canvas):
        pass
