# pytetris/src/game/board.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from tetronimo import *


class BoardWidget(QWidget):
    def __init__(self, board_width=10, board_height=20, cell_size=30, parent=None):
        super().__init__(parent)
        self.board_width = board_width
        self.board_height = board_height
        self.cell_size = cell_size
        self.grid = [[None for _ in range(board_width)] for _ in range(board_height)]
        self.active_piece = None
        self.score = 0
        self.level = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        self.render(painter)

    def render(self, painter):
        # Render grid
        for row in range(self.board_height):
            for col in range(self.board_width):
                if self.grid[row][col] is not None:
                    painter.fillRect(col * self.cell_size, row * self.cell_size,
                                     self.cell_size, self.cell_size,
                                     QColor(self.grid[row][col]))
        # render piece
        piece = self.active_piece
        if piece is not None:
            for row in range(len(piece.shape)):
                for col in range(len(piece.shape[row])):
                    if piece.shape[row][col] == 1:
                        x = (piece.position[0] + col) * self.cell_size
                        y = (piece.position[1] + row) * self.cell_size
                        painter.fillRect(x, y, self.cell_size, self.cell_size, QColor(piece.color))
        return

    def place_piece(self, tetronimo):
        start_x_position = (self.board_width - len(tetronimo.shape[0])) // 2
        tetronimo.position = (start_x_position, 0)

        for row in range(len(tetronimo.shape)):
            for col in range(len(tetronimo.shape[row])):
                if tetronimo.shape[row][col] == 1:
                    self.grid[row][start_x_position + col] = tetronimo.color
        self.active_piece = tetronimo

        return

    def move_piece(self, direction):
        if direction == 'left':
            new_position = (self.active_piece.position[0] - 1, self.active_piece.position[1])
        elif direction == 'right':
            new_position = (self.active_piece.position[0] + 1, self.active_piece.position[1])
        elif direction == 'down':
            new_position = (self.active_piece.position[0], self.active_piece.position[1] + 1)
        else:
            return
        if not self.check_collision(new_position):
            self.active_piece.position = new_position
            self.update()
        else:
            if direction == 'down':
                self.place_piece(self.active_piece)
        return

    def rotate_piece(self):
        return

    def check_collision(self, shape, position):
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col] == 1:
                    x = position[0] + col
                    y = position[1] + row
                    if x < 0 or x >= self.board_width or y >= self.board_height:
                        return True
                    if self.grid[y][x] is not None:
                        return True
        return False

    def clear_lines(self):
        full_rows = []
        for row in range(self.board_height):
            if all(self.grid[row][col] is not None for col in range(self.board_width)):
                full_rows.append(row)

        for row in full_rows:
            del self.grid[row]
            self.grid.insert(0, [None for _ in range(self.board_width)])

        self.score += len(full_rows) * 100
        return

    def reset_game(self):
        return

    def game_over(self):
        self.reset_game()
        return
