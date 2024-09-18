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
        self.right_layout = None
        self.left_layout = None
        self.main_layout = None
        self.lines_label = None
        self.bottom_spcr = None
        self.time_label = None
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

        # Create the main horizontal layout
        self.main_layout = QHBoxLayout()

        # LEFT SIDE: Game title, board, and controls (vertically stacked)
        self.left_layout = QVBoxLayout()

        # Title label
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_layout.addWidget(self.title_label)

        # Start Game button (visible on start)
        self.start_button = QPushButton("Start Game")
        self.start_button.setFixedSize(150, 50)
        self.start_button.clicked.connect(self.start_game)  # Connect the start button to the game start logic
        self.left_layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Board widget (initially hidden, centered)
        self.board.setVisible(False)
        self.left_layout.addWidget(self.board, alignment=Qt.AlignmentFlag.AlignCenter)
        self.bottom_spcr = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.left_layout.addItem(self.bottom_spcr)

        # Add left layout to the main layout
        self.main_layout.addLayout(self.left_layout)

        # Add a horizontal spacer between the left and right layouts
        column_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed,
                                    QSizePolicy.Policy.Minimum)  # 40 pixels wide spacer
        self.main_layout.addSpacerItem(column_spacer)

        # RIGHT SIDE: Game info (Score, Level, etc.)
        self.right_layout = QVBoxLayout()

        # Info labels for Score, Level, Time, and Lines Cleared
        self.score_label = QLabel("Score: 0")
        self.level_label = QLabel("Level: 1")
        self.time_label = QLabel("Time: 00:00")
        self.lines_label = QLabel("Lines Cleared: 0")

        # Add the info labels to the right layout
        self.right_layout.addWidget(self.score_label)
        self.right_layout.addWidget(self.level_label)
        self.right_layout.addWidget(self.time_label)
        self.right_layout.addWidget(self.lines_label)

        # Add right layout to the main layout
        self.main_layout.addLayout(self.right_layout)

        # Hide the right layout initially
        self.hide_right_layout()

        # Set margins for the left and right layouts
        self.left_layout.setContentsMargins(20, 0, 20, 0)  # Add 20px margin to the right of the left layout
        self.right_layout.setContentsMargins(0, 0, 20, 0)  # Add 20px margin to the left of the right layout

        # Set the layout for the central widget
        central_widget.setLayout(self.main_layout)

        # Connect game timer and other signals as needed
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

    def hide_right_layout(self):
        """
        Hide all widgets in the right layout (Score, Level, Time, Lines Cleared).
        """
        for i in reversed(range(self.right_layout.count())):  # Loop through the right layout widgets
            widget = self.right_layout.itemAt(i).widget()
            if widget is not None:
                widget.hide()  # Hide each widget

    def show_right_layout(self):
        """
        Show all widgets in the right layout (Score, Level, Time, Lines Cleared).
        """
        for i in reversed(range(self.right_layout.count())):  # Loop through the right layout widgets
            widget = self.right_layout.itemAt(i).widget()
            if widget is not None:
                widget.show()  # Show each widget

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
        # Show the score and game info labels on the right
        # Show the right layout (score and game info labels)
        self.show_right_layout()

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
