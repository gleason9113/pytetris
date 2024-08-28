# pytetris/src/game/tetronimo.py
from board import BoardWidget
class Tetronimo:
    def __init__(self, shape, color):
        self.shape = shape
        self.rotation_state = 0
        self.color = color
        self.position = None

    def rotate(self):
        self.rotation_state = (self.rotation_state + 1) % 4


class Itetronimo(Tetronimo):
    def __init__(self):
        shape = [
            [1, 1, 1, 1]
        ]
        color = "cyan"  # Pick better colors later
        super().__init__(shape, color)

    def rotate_right(self):
        if self.rotation_state % 2 == 0:
            return [
                [1, 1, 1, 1]
            ]
        else:
            return [
                [1],
                [1],
                [1],
                [1]
            ]

    def rotate_left(self):
        return self.rotate_right()
