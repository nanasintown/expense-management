from PyQt6.QtWidgets import QLineEdit


class LineEditWidget(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def focusInEvent(self, event) -> None:
        self.clear()
        QLineEdit.focusInEvent(self, event)
        self.setStyleSheet("color: rgba(0, 0, 0, 100)")
