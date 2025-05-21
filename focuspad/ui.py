from pathlib import Path
from datetime import datetime
import logging
import json

# Qt imports with fallback between PySide6 and PyQt6
try:
    from PySide6.QtWidgets import (
        QWidget, QTextEdit, QVBoxLayout, QHBoxLayout,
        QPushButton, QApplication, QLabel, QLineEdit,
        QDateEdit, QGroupBox, QCheckBox, QListWidget
    )
    from PySide6.QtCore import Qt, QTimer, QDate
    from PySide6.QtGui import QIcon, QPixmap, QMouseEvent
except ModuleNotFoundError:
    from PyQt6.QtWidgets import (
        QWidget, QTextEdit, QVBoxLayout, QHBoxLayout,
        QPushButton, QApplication, QLabel, QLineEdit,
        QDateEdit, QGroupBox, QCheckBox, QListWidget
    )
    from PyQt6.QtCore import Qt, QTimer, QDate
    from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent

# Configure logging
logger = logging.getLogger("focuspad.ui")
# Ensure save directory exists
SAVE_DIR = Path(__file__).resolve().parent / "entries"
SAVE_DIR.mkdir(exist_ok=True)
logger.info(f"Journal entries directory: {SAVE_DIR}")

class JournalWidget(QWidget):
    def __init__(self):
        super().__init__()
        logger.debug("Initializing JournalWidget")

        # Enable dragging variables
        self._drag_pos = None

        # Window setup (frameless)
        self.setWindowTitle("FocusPad")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setFixedSize(900, 600)

        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ─── Left Sidebar ─────────────────────────────────────────
        sidebar = QVBoxLayout()
        sidebar.setContentsMargins(8, 8, 8, 8)
        sidebar.setSpacing(10)

        # Logo
        logo_label = QLabel()
        logo_path = Path(__file__).resolve().parent / "assets" / "focuspad.png"
        if logo_path.exists():
            pix = QPixmap(str(logo_path))
            logo_label.setPixmap(pix.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            logo_label.setText("[FocusPad Logo]")
        logo_label.setAlignment(Qt.AlignCenter)
        sidebar.addWidget(logo_label)

        # Greeting
        greet = QLabel("Hi, Sridhar!")
        greet.setAlignment(Qt.AlignCenter)
        sidebar.addWidget(greet)

        # Pad list
        self.pad_list = QListWidget()
        self.pad_list.setToolTip("Select a saved journal entry")
        sidebar.addWidget(self.pad_list)

        # Controls: New + Settings
        ctrl_row = QHBoxLayout()
        self.add_btn = QPushButton()
        add_icon_path = Path(__file__).resolve().parent / "assets" / "add_icon.png"
        if add_icon_path.exists():
            self.add_btn.setIcon(QIcon(str(add_icon_path)))
        else:
            self.add_btn.setText("+")
        self.add_btn.setToolTip("New journal page")
        self.add_btn.clicked.connect(self.new_page)
        ctrl_row.addWidget(self.add_btn)

        self.settings_btn = QPushButton()
        set_icon_path = Path(__file__).resolve().parent / "assets" / "settings_icon.png"
        if set_icon_path.exists():
            self.settings_btn.setIcon(QIcon(str(set_icon_path)))
        else:
            self.settings_btn.setText("⚙")
        self.settings_btn.setToolTip("Settings")
        ctrl_row.addWidget(self.settings_btn)

        sidebar.addLayout(ctrl_row)

        # Badges placeholder
        badge_label = QLabel("Badges")
        badge_label.setAlignment(Qt.AlignCenter)
        sidebar.addWidget(badge_label)

        # Populate list
        self.load_pads()
        main_layout.addLayout(sidebar)

        # ─── Right Content ────────────────────────────────────────
        content = QVBoxLayout()
        content.setContentsMargins(8, 8, 8, 8)
        content.setSpacing(10)

        # Top: pad name, date, day
        top = QHBoxLayout()
        self.pad_name_edit = QLineEdit()
        self.pad_name_edit.setPlaceholderText("Pad Name")
        top.addWidget(self.pad_name_edit)

        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.setReadOnly(True)
        top.addWidget(self.date_edit)

        self.day_label = QLabel(QDate.currentDate().toString("dddd"))
        top.addWidget(self.day_label)
        content.addLayout(top)

        # Morning pad
        self.morning_checks = []
        morning = QGroupBox("Morning Pad")
        mlay = QVBoxLayout()
        self.morning_text = QTextEdit()
        self.morning_text.setPlaceholderText("Enter morning goals...")
        mlay.addWidget(self.morning_text)
        for i in range(3):
            cb = QCheckBox(f"Goal {i+1}")
            mlay.addWidget(cb)
            self.morning_checks.append(cb)
        morning.setLayout(mlay)
        content.addWidget(morning)

        # Night pad
        self.night_checks = []
        night = QGroupBox("Night Pad")
        nlay = QVBoxLayout()
        self.night_text = QTextEdit()
        self.night_text.setPlaceholderText("Reflect on your day...")
        nlay.addWidget(self.night_text)
        for label in ["Exercise", "Study", "Upskill", "Junk Food"]:
            cb = QCheckBox(label)
            nlay.addWidget(cb)
            self.night_checks.append(cb)
        night.setLayout(nlay)
        content.addWidget(night)

        # Bottom: Save & Close
        bottom = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.manual_save)
        bottom.addWidget(save_btn)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(QApplication.instance().quit)
        bottom.addWidget(close_btn)
        content.addLayout(bottom)
        main_layout.addLayout(content)

        # Autosave
        self.autosave = QTimer(self, interval=300_000, timeout=self.save_entry)
        self.autosave.start()

        # Create initial default page
        self.new_page(initial=True)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._drag_pos is not None and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._drag_pos = None

    def load_pads(self):
        """Load existing JSON entries into the sidebar."""
        self.pad_list.clear()
        for file in sorted(SAVE_DIR.glob("*.json")):
            try:
                data = json.loads(file.read_text(encoding="utf-8"))
                name = data.get("pad_name", file.stem)
                date = data.get("date", "")
                self.pad_list.addItem(f"{name} ({date})")
            except Exception:
                continue

    def new_page(self, initial=False):
        """Create a new journal page default name."""
        today = QDate.currentDate().toString("yyyy-MM-dd")
        existing = []
        for file in SAVE_DIR.glob("*.json"):
            try:
                d = json.loads(file.read_text(encoding="utf-8"))
                if d.get("date") == today:
                    existing.append(d.get("pad_name"))
            except:
                pass
        i = 1
        while f"Journal Page {i}" in existing:
            i += 1
        default_name = f"Journal Page {i}"
        self.pad_name_edit.setText(default_name)
        if not initial:
            self.morning_text.clear()
            self.night_text.clear()
            for cb in self.morning_checks + self.night_checks:
                cb.setChecked(False)
        self.autosave.stop()
        self.autosave.start()

    def save_entry(self):
        pad_name = self.pad_name_edit.text().strip() or "Untitled"
        date = self.date_edit.date().toString("yyyy-MM-dd")
        data = {
            "pad_name": pad_name,
            "date": date,
            "morning": {
                "text": self.morning_text.toPlainText(),
                "checks": [{"label": cb.text(), "checked": cb.isChecked()} for cb in self.morning_checks]
            },
            "night": {
                "text": self.night_text.toPlainText(),
                "checks": [{"label": cb.text(), "checked": cb.isChecked()} for cb in self.night_checks]
            }
        }
        fname = f"{pad_name.replace(' ', '_')}_{date}.json"
        out = SAVE_DIR / fname
        out.write_text(json.dumps(data, indent=2), encoding="utf-8")
        logger.info(f"Saved journal: {out}")
        self.load_pads()

    def manual_save(self):
        self.save_entry()
        self.autosave.stop()
        self.autosave.start()
