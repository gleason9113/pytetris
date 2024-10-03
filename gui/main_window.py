# pytetris/gui/main_window.py
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QSpacerItem,
                             QSizePolicy)
from src.game.board import BoardWidget
from .utils import print_layout_info


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.level = None
        self.lines_cleared = None
        self.score = None
        self.btn_brd_spcr = None
        self.right_layout = None
        self.left_layout = None
        self.main_layout = None
        self.lines_label = None
        self.bottom_spcr = None
        self.time_label = None
        self.level_label = None
        self.score_label = None
        self.elapsed_time = 0
        self.ui_update_timer = QTimer()
        self.title_label = QLabel("PyTetris")
        self.board = BoardWidget()
        self.game_timer = QTimer()
        self.start_button = QPushButton("Start Game")
        self.setWindowTitle("PyTetris")
        self.setGeometry(100, 100, 400, 800)
        self.initUI()
        self.apply_styles()
        self.setFocus()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.ui_update_timer.timeout.connect(self.update_timer_label)  # Call every second
        self.ui_update_timer.start(1000)  # Fire every 1000 milliseconds (1 second)
        print(f"MainWindow focus: {self.hasFocus()}")

    def initUI(self):
        # Create the central widget and set the layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create the main vertical layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 20, 0, 0)  # Margins around the layout

        # Create the info layout
        self.score_label = QLabel("Score: 0")
        self.score_label.setContentsMargins(0, 10, 0, 10)
        self.lines_label = QLabel("Lines Cleared: 0")
        self.lines_label.setContentsMargins(0, 10, 0, 10)
        self.level_label = QLabel("Level: 0")
        self.level_label.setContentsMargins(0, 10, 0, 10)
        self.time_label = QLabel("Time: 00:00")
        self.time_label.setContentsMargins(0, 10, 0, 10)

        # Create and organize the game state information layout
        gamestate_layout = QVBoxLayout()
        gamestate_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        gamestate_layout.addWidget(self.score_label, alignment=Qt.AlignmentFlag.AlignCenter)
        gamestate_layout.addWidget(self.time_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Inner layout for lines and level info
        inner_layout = QHBoxLayout()
        inner_layout.addWidget(self.lines_label, alignment=Qt.AlignmentFlag.AlignCenter)
        inner_layout.addWidget(self.level_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add layouts to the main game state layout
        gamestate_layout.addLayout(inner_layout)
        layout.addLayout(gamestate_layout)

        # Start Button (centered)
        self.start_button.setFixedSize(150, 50)
        self.start_button.clicked.connect(self.start_game)
        layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Spacer between the start button and the board
        self.btn_brd_spcr = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        layout.addItem(self.btn_brd_spcr)

        # Board widget (initially hidden, centered)
        self.board.setVisible(False)
        layout.addWidget(self.board, alignment=Qt.AlignmentFlag.AlignCenter)

        # Set the layout for the central widget
        central_widget.setLayout(layout)

        # Print layout info (debugging only)
        print_layout_info(self.centralWidget())

        # Connect the game timer to the board's move_piece_down method
        self.game_timer.timeout.connect(self.board.move_piece_down)

    def update_score_label(self):
        """
        Update the score label with the current score.
        """
        self.score_label.setText(f"Score: {self.score}")

    def update_lines_label(self):
        """
        Update the lines cleared label with the current number of lines cleared.
        """
        self.lines_label.setText(f"Lines Cleared: {self.lines_cleared}")

    def update_level_label(self):
        """
        Update the level label with the current level.
        """
        self.level_label.setText(f"Level: {self.level}")

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #353535;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #FFFFFF;
            }
            BoardWidget {
                background-color: #A9A9A9;
                border: 2px solid #FFFFFF;
            }
        """)

    def update_timer_label(self):
        """
        Update the timer_label to show elapsed time in MM:SS format.
        """
        self.elapsed_time += 1  # Increment elapsed time by 1 second
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        self.time_label.setText(f"Time: {minutes:02}:{seconds:02}")  # Format as MM:SS

    def keyPressEvent(self, event):
        """
        Handle key press events for game input.
        :param event: QKeyEvent - key press information.
        :return: None.
        """
        if event.key() == Qt.Key.Key_Left:
            self.board.move_piece('left')
        elif event.key() == Qt.Key.Key_Right:
            self.board.move_piece('right')
        elif event.key() == Qt.Key.Key_Up:
            self.board.rotate_piece('right')
        elif event.key() == Qt.Key.Key_Down:
            self.board.move_piece('down')
        elif event.key() == Qt.Key.Key_Space:
            self.toggle_pause()

    def start_game_loop(self):
        """
        Start or resume the game loop, moving the active piece down at timed intervals.
        :return: None
        """
        try:
            self.game_timer.timeout.disconnect()
        except TypeError:
            pass
        self.board.level = max(self.board.level, 1)

        self.game_timer.timeout.connect(self.board.move_piece_down)
        interval = 1000 // self.board.level
        self.game_timer.start(interval)

    def stop_game_loop(self):
        """
        Pauses the game loop.
        :return: None
        """
        self.game_timer.stop()

    def start_game(self):
        """
        Starts a new game by resetting the board and adding the first piece.
        :return: None.
        """
        print("start_game called")
        self.board.reset_game()
        self.board.is_paused = False
        self.start_button.hide()
        layout = self.centralWidget().layout()
        self.board.setVisible(True)

        layout.activate()
        self.update()
        print_layout_info(self.centralWidget())
        self.start_game_loop()

    def pause_game_key(self, event):
        """
        Handles key press event - pause/unpause game with Space key.
        :param event:
        :return: None
        """
        if event.key() == Qt.Key.Key_Space:
            self.toggle_pause()

    def toggle_pause(self):
        """
        Toggles game pause.
        :return: None
        """
        if self.board.is_paused:
            self.board.is_paused = False
            self.start_game_loop()
        else:
            self.board.is_paused = True
            self.stop_game_loop()
