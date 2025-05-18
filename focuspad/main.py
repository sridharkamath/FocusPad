from PySide6.QtWidgets import QApplication
from ui import JournalWidget
from reminder import schedule_reminder

def main():
    app = QApplication([])
    schedule_reminder()
    JournalWidget().show()
    app.exec()

if __name__ == "__main__":
    main()
