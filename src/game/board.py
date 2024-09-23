# pytetris/src/game/board.py
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen
from .tetronimo import *


class BoardWidget(QWidget):
    """
    A widget representing the game board.

    Handles rendering the Tetris board, managing the game grid, and rotation, movement, and placement of pieces.

    Attributes:
        board_width (int): Width of game board in cells.
        board_height (int): Height of game board in cells.
        cell_size (int):  Size of cells in pixels.
        grid (list):  A 2D list representing the current board state.
        active_piece (Tetronimo): The current piece in play.
        score (int): Player score for current game.
        level (int): Current level.
    """

    def __init__(self, board_width=10, board_height=20, cell_size=30, parent=None):
        super().__init__(parent)
        self.board_width = board_width
        self.board_height = board_height
        self.cell_size = cell_size
        self.grid = [[None for _ in range(board_width)] for _ in range(board_height)]
        self.active_piece = None
        self.score = 0
        self.level = 0
        self.is_paused = False
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.setFixedSize(self.board_width * self.cell_size, self.board_height * self.cell_size)

        print(f"BoardWidget size: {self.size()}")
        print(f"BoardWidget geometry: {self.geometry()}")

    def paintEvent(self, event):
        """
        Handles the widget's paint event by rendering the current board state.
        :param event: (QPaintEvent) The paint event object containing details about the repaint request.
        :return: None
        """
        # print("paintEvent called!")
        painter = QPainter(self)
        try:
            # Board styles
            painter.fillRect(self.rect(), QColor("#A9A9A9"))
            # Set the color and pen for gridlines
            pen = QPen(QColor("#555555"))  # Dark gray gridlines
            pen.setWidth(1)
            painter.setPen(pen)

            # Draw horizontal and vertical gridlines
            for row in range(self.board_height + 1):  # Draw horizontal lines
                y = row * self.cell_size
                painter.drawLine(0, y, self.board_width * self.cell_size, y)

            for col in range(self.board_width + 1):  # Draw vertical lines
                x = col * self.cell_size
                painter.drawLine(x, 0, x, self.board_height * self.cell_size)

            self.draw_board(painter)
        finally:
            painter.end()


    def draw_board(self, painter):
        """
        Draws the current state of the Tetris board.

        :param painter: (QPainter) The QPainter object used for drawing the board.
        :return: None.
        """
        # print("draw_board called!")
        # Render grid
        for row in range(self.board_height):
            for col in range(self.board_width):
                if self.grid[row][col] is not None:  # Cell is occupied
                    painter.fillRect(col * self.cell_size, row * self.cell_size,
                                     self.cell_size, self.cell_size,
                                     QColor(self.grid[row][col]))
        # render piece
        piece = self.active_piece
        if piece is not None:
            for row in range(len(piece.shape)):
                for col in range(len(piece.shape[row])):
                    if piece.shape[row][col] == 1:  # Calculate x and y coordinates and fill the cell.
                        x = (piece.position[0] + col) * self.cell_size
                        y = (piece.position[1] + row) * self.cell_size
                        painter.fillRect(x, y, self.cell_size, self.cell_size, QColor(piece.color))
        return

    def get_random_piece(self):
        """
           Generates a random Tetronimo piece.
           :return: A random Tetronimo object.
           """
        import random
        tetronimoes = [Itetronimo, OTetronimo, TTetronimo, LTetronimo, JTetronimo, STetronimo, ZTetronimo]
        return random.choice(tetronimoes)()

    def place_piece(self, tetronimo):
        """
        Adds a new piece to the board at the starting position.
        :param tetronimo: (Tetronimo) The game piece to be added at the starting position.
        :return: None
        """
        x_position = (self.board_width - len(tetronimo.shape[0])) // 2
        tetronimo.position = (x_position, 0)  # Starts at top center of board.

        for row in range(len(tetronimo.shape)):
            for col in range(len(tetronimo.shape[row])):
                if tetronimo.shape[row][col] == 1:
                    self.grid[row][x_position + col] = tetronimo.color
        self.active_piece = tetronimo

    def clear_active_piece(self):
        """
        Clears the active piece from the grid to allow it to move to a new position without leaving a trail.
        :return: None.
        """
        for row in range(len(self.active_piece.shape)):
            for col in range(len(self.active_piece.shape[row])):
                if self.active_piece.shape[row][col] == 1:
                    x = self.active_piece.position[0] + col
                    y = self.active_piece.position[1] + row
                    if 0 <= x < self.board_width and 0 <= y < self.board_height:
                        self.grid[y][x] = None  # Clear the previous position in the grid

    def move_piece(self, direction):
        """
        Moves the active piece in the specified direction.
        :param direction: (str) The direction to move: 'left', 'right', or 'down'.
        :return: None.
        """
        print(f"move_piece called:  {direction}")
        if direction == 'left':
            new_position = (self.active_piece.position[0] - 1, self.active_piece.position[1])
        elif direction == 'right':
            new_position = (self.active_piece.position[0] + 1, self.active_piece.position[1])
        elif direction == 'down':
            self.move_piece_down()
            return
        else:
            return  # Whatever was passed, it wasn't a valid direction.

        if not self.check_collision(self.active_piece.shape, new_position):
            self.active_piece.position = new_position
            self.update()
        else:
            if direction == 'down':
                self.place_piece(self.active_piece)
        self.update()
        return

    def move_piece_down(self):
        """
        Moves the active piece down one cell.  If a collision is detected, the piece is placed at that point.
        :return: None.
        """
        # print(f"move_piece_down called! Current position: {self.active_piece.position}")
        self.clear_active_piece()
        new_position = (self.active_piece.position[0], self.active_piece.position[1] + 1)
        if not self.check_collision(self.active_piece.shape, new_position):
            self.active_piece.position = new_position
            print(f"New position after move: {self.active_piece.position}")
            self.update()
        else:
            self.place_piece(self.active_piece)
        self.update()

    def rotate_piece(self, direction='right'):
        """
        Rotates the active piece in the indicated direction.
        :param direction: (str) The direction to rotate the piece in.
        :return: None.
        """
        rotated_piece = None
        if self.active_piece is None:
            return
        if direction == 'right':
            rotated_shape = self.active_piece.rotate_right()
        elif direction == 'left':
            rotated_shape = self.active_piece.rotate_left()
        else:
            return

        if not self.check_collision(rotated_shape, self.active_piece.position):
            self.active_piece.shape = rotated_shape
            self.active_piece.rotate()
            self.update()
        else:
            pass

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
        """
        Resets the game state, clearing board, level, and score. Adds initial piece and pauses the game.
        :return: None.
        """
        print("reset_game called")
        self.grid = [[None for _ in range(self.board_width)] for _ in range(self.board_height)]
        self.active_piece = None
        self.score = 0
        self.level = 1
        self.is_paused = True

        self.place_piece(self.get_random_piece())
        self.update()

    def game_over(self):
        self.reset_game()
        return
