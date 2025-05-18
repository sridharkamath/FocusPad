from pathlib import Path
from datetime import datetime
from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PySide6.QtCore import Qt, QTimer

SAVE_DIR = Path.home() / "FocusPadEntries"
SAVE_DIR.mkdir(exist_ok=True)

class JournalWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FocusPad")
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool
        )
        self.setFixedSize(320, 220)

        layout = QVBoxLayout(self)
        self.editor = QTextEdit(placeholderText="Stay focused… jot your thoughts")
        layout.addWidget(self.editor)

        # autosave every 60 s
        self.autosave = QTimer(self, interval=60_000, timeout=self.save_entry)
        self.autosave.start()

    def save_entry(self):
        today = datetime.now().strftime("%Y-%m-%d")
        (SAVE_DIR / f"{today}.md").write_text(self.editor.toPlainText(), "utf-8")
