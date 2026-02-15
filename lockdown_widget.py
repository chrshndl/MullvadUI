from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox
import mullvad_cli


class LockdownQtWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.status = QLabel("Lockdown: loading…")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setStyleSheet("font-size: 16px; font-weight: 600;")
        layout.addWidget(self.status)

        self.toggle_btn = QPushButton("Toggle")
        self.toggle_btn.clicked.connect(self.on_toggle)
        layout.addWidget(self.toggle_btn)

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh)
        layout.addWidget(self.refresh_btn)

        self.refresh()

    def refresh(self):
        try:
            enabled = mullvad_cli.get_lockdown_state()
            if enabled:
                self.status.setText("Lockdown: ON 🔒")
                self.toggle_btn.setText("Turn OFF")
            else:
                self.status.setText("Lockdown: OFF 🔓")
                self.toggle_btn.setText("Turn ON")
        except Exception as e:
            self.status.setText("Lockdown: ERROR")
            QMessageBox.critical(self, "Mullvad Error", str(e))

    def on_toggle(self):
        try:
            current = mullvad_cli.get_lockdown_state()
            mullvad_cli.set_lockdown_state(not current)
            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, "Mullvad Error", str(e))
