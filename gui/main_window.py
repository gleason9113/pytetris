# pytetris/gui/main_window.py
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QSpacerItem,
                             QSizePolicy, QFrame)
from src.game.board import BoardWidget


class MainWindow(QMainWindow):
    def wrap_in_frame(self, widget):
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setLineWidth(2)
        widget.setParent(frame)
        return frame

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
        # Create the central widget and set the layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create the main vertical layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 20, 0, 0)  # Margins around the layout

        # Title Label (centered)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Centers label horizontally, not vertically
        layout.addWidget(self.title_label)

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

        # Connect the game timer to the board's move_piece_down method
        self.game_timer.timeout.connect(self.board.move_piece_down)

        # Debug prints for widget geometry
        print(f"Title Label Geometry: {self.title_label.geometry()}")
        print(f"Start Button Geometry: {self.start_button.geometry()}")
        print(f"Board Widget Geometry: {self.board.geometry()}")

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
        print("start_game called")
        self.board.reset_game()
        self.board.is_paused = False
        self.start_button.hide()
        layout = self.centralWidget().layout()
        # layout.removeItem(self.btn_brd_spcr)  # Remove the old spacer
        # layout.addItem(
        #    QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))  # Add a zero-height spacer
        self.board.setVisible(True)
        layout.activate()
        self.update()
        print(f"Board Widget Geometry after start: {self.board.geometry()}")

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
