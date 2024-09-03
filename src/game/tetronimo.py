# pytetris/src/game/tetronimo.py


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


class OTetronimo(Tetronimo):
    def __init__(self):
        shape = [
            [1, 1],
            [1, 1]
        ]
        color = "yellow"
        super().__init__(shape, color)

    def rotate_right(self):
        return self.shape  # No change

    def rotate_left(self):
        return self.shape  # No change


class TTetronimo(Tetronimo):
    def __init__(self):
        shape = [
            [0, 1, 0],
            [1, 1, 1]
        ]
        color = "purple"
        super().__init__(shape, color)

    def rotate_right(self):
        if self.rotation_state == 0:
            return [
                [1, 0],
                [1, 1],
                [1, 0]
            ]
        elif self.rotation_state == 1:
            return [
                [1, 1, 1],
                [0, 1, 0]
            ]
        elif self.rotation_state == 2:
            return [
                [0, 1],
                [1, 1],
                [0, 1]
            ]
        else:
            return [
                [0, 1, 0],
                [1, 1, 1]
            ]

    def rotate_left(self):
        return self.rotate_right()


class LTetronimo(Tetronimo):
    def __init__(self):
        shape = [
            [1, 0, 0],
            [1, 1, 1]
        ]
        color = "orange"
        super().__init__(shape, color)

    def rotate_right(self):
        if self.rotation_state == 0:
            return [
                [1, 1],
                [1, 0],
                [1, 0]
            ]
        elif self.rotation_state == 1:
            return [
                [1, 1, 1],
                [0, 0, 1]
            ]
        elif self.rotation_state == 2:
            return [
                [0, 1],
                [0, 1],
                [1, 1]
            ]
        else:
            return [
                [1, 0, 0],
                [1, 1, 1]
            ]

    def rotate_left(self):
        return self.rotate_right()


class JTetronimo(Tetronimo):
    def __init__(self):
        shape = [
            [0, 0, 1],
            [1, 1, 1]
        ]
        color = "blue"
        super().__init__(shape, color)

    def rotate_right(self):
        if self.rotation_state == 0:
            return [
                [1, 0],
                [1, 0],
                [1, 1]
            ]
        elif self.rotation_state == 1:
            return [
                [1, 1, 1],
                [1, 0, 0]
            ]
        elif self.rotation_state == 2:
            return [
                [1, 1],
                [0, 1],
                [0, 1]
            ]
        else:
            return [
                [0, 0, 1],
                [1, 1, 1]
            ]

    def rotate_left(self):
        return self.rotate_right()


class STetronimo(Tetronimo):
    def __init__(self):
        shape = [
            [0, 1, 1],
            [1, 1, 0]
        ]
        color = "green"
        super().__init__(shape, color)

    def rotate_right(self):
        if self.rotation_state % 2 == 0:
            return [
                [1, 0],
                [1, 1],
                [0, 1]
            ]
        else:
            return [
                [0, 1, 1],
                [1, 1, 0]
            ]

    def rotate_left(self):
        return self.rotate_right()


class ZTetronimo(Tetronimo):
    def __init__(self):
        shape = [
            [1, 1, 0],
            [0, 1, 1]
        ]
        color = "red"
        super().__init__(shape, color)

    def rotate_right(self):
        if self.rotation_state % 2 == 0:
            return [
                [0, 1],
                [1, 1],
                [1, 0]
            ]
        else:
            return [
                [1, 1, 0],
                [0, 1, 1]
            ]

    def rotate_left(self):
        return self.rotate_right()
