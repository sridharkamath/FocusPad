from PySide6.QtWidgets import QApplication
from ui import JournalWidget
from reminder import schedule_reminder
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)5s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger("focuspad")

def main():
    logger.info("▶ Starting FocusPad")

    schedule_reminder()
    logger.debug("Scheduled reminders thread started")

    app = QApplication([])
    widget = JournalWidget()
    logger.debug("JournalWidget initialized, about to show()")
    widget.show()
    logger.info("Widget shown – entering Qt event loop")
    app.exec()
    logger.info("Qt event loop exited, shutting down")


if __name__ == "__main__":
    main()
