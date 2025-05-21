from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt


class DashboardWidget(QWidget):
    """
    Dashboard on the left sidebar showing a list of pads/journals,
    and quick actions (add pad, settings), plus a summary of streaks/badges.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        # Title
        title = QLabel("Dashboard")
        title.setObjectName("dashboardTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # List of pads/journals
        self.pad_list = QListWidget()
        self.pad_list.setObjectName("padList")
        layout.addWidget(self.pad_list)

        # Quick action buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(5)

        self.add_btn = QPushButton()
        self.add_btn.setIcon(QIcon("assets/add_icon.png"))
        self.add_btn.setIconSize(QSize(24, 24))
        self.add_btn.setToolTip("Add new pad")
        self.add_btn.setObjectName("addPadButton")
        btn_layout.addWidget(self.add_btn)

        self.settings_btn = QPushButton()
        self.settings_btn.setIcon(QIcon("assets/settings_icon.png"))
        self.settings_btn.setIconSize(QSize(24, 24))
        self.settings_btn.setToolTip("Settings")
        self.settings_btn.setObjectName("settingsButton")
        btn_layout.addWidget(self.settings_btn)

        layout.addLayout(btn_layout)

        # Section for streaks & badges summary
        badge_label = QLabel("Streaks & Badges")
        badge_label.setObjectName("badgeSectionLabel")
        layout.addWidget(badge_label)

        # Placeholder widget for badges (e.g., grid or flow layout)
        # TODO: implement BadgeContainerWidget for actual badges
        # self.badge_container = BadgeContainerWidget()
        # layout.addWidget(self.badge_container)

        self.setLayout(layout)
