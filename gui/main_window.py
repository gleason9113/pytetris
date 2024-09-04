# pytetris/gui/main_window.py
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QSpacerItem,
                             QSizePolicy)
from src.game.board import BoardWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.level_label = None
        self.score_label = None
        self.title_label = QLabel("PyTetris")
        self.board = BoardWidget()
        self.game_timer = QTimer()
        self.start_button = QPushButton("Start Game")
        self.setWindowTitle("PyTetris")
        self.setGeometry(100, 100, 400, 800)
        self.initUI()
        self.apply_styles()

    def initUI(self):
        # Create layout and displays
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 20, 0, 0)

        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        # Add a spacer above the button to push it towards the center vertically
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.start_button.setFixedSize(150, 50)
        layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        #        label_layout = QHBoxLayout()  # Container for score and level
        #        label_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #        label_layout.addWidget(self.score_label)
        #        label_layout.addWidget(self.level_label)
        #        layout.addLayout(label_layout)

        layout.addWidget(self.board)

        central_widget.setLayout(layout)

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
                background-color: #202020;
                border: 2px solid #FFFFFF;
            }
        """)

    def start_game_loop(self):
        """
        Start or resume the game loop, moving the active piece down at timed intervals.
        :return: None
        """
        self.game_timer.disconnect()
        if not self.game_timer.isActive():
            self.game_timer.connect(self.board.move_piece_down)
        self.game_timer.start(1000 // self.board.level)

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
        self.board.reset_game()
        self.board.is_paused = False

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
