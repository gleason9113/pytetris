# pytetris/gui/main_window.py
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel
from src.game.board import BoardWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.level_label = None
        self.score_label = None
        self.board = None
        self.setWindowTitle("PyTetris")
        self.setGeometry(100, 100, 400, 800)
        self.initUI()
        self.apply_styles()

    def initUI(self):
        # Create layout and displays
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        label_layout = QHBoxLayout() # Container for score and level
        label_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_label = QLabel("Score: 0")
        self.level_label = QLabel("Level: 1")
        label_layout.addWidget(self.score_label)
        label_layout.addWidget(self.level_label)
        layout.addLayout(label_layout)
        self.board = BoardWidget()
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
