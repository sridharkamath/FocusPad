from pathlib import Path
from datetime import datetime
from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QPushButton, QApplication
from PySide6.QtCore import Qt, QTimer
import logging

# ─── Configure module‐level logger ─────────────────────────────
logger = logging.getLogger("focuspad.ui")

SAVE_DIR = Path(__file__).resolve().parent / "entries"
SAVE_DIR.mkdir(exist_ok=True)
logger.info(f"Journal entries directory: {SAVE_DIR}")

class JournalWidget(QWidget):
    def __init__(self):
        super().__init__()
        logger.debug("Initializing JournalWidget")
        self.setWindowTitle("FocusPad")
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool
        )
        self.setFixedSize(320, 220)

        layout = QVBoxLayout(self)
        
        # ─── Text editor ────────────────────────────────────
        self.editor = QTextEdit(placeholderText="Stay focused… jot your thoughts")
        layout.addWidget(self.editor)

        # ─── Close button ───────────────────────────────────
        close_btn = QPushButton("Close")
        close_btn.setToolTip("Close FocusPad and exit")
        close_btn.clicked.connect(QApplication.instance().quit)
        layout.addWidget(close_btn)

        # ─── Autosave timer ────────────────────────────────
        logger.debug("Starting autosave timer (60s)")
        self.autosave = QTimer(self, interval=60_000, timeout=self.save_entry)
        self.autosave.start()

    def save_entry(self):
        text = self.editor.toPlainText()
        today = datetime.now().strftime("%Y-%m-%d")
        out = SAVE_DIR / f"{today}.md"

        logger.debug(f"Saving entry ({len(text)} chars) to {out.name}")
        out.write_text(text, encoding="utf-8")
        logger.info(f"Wrote {len(text)} chars to {out}")
