import sys
from PySide6.QtCore import Qt
from lockdown_widget import LockdownQtWidget
from connect_disconnect import ConnectDisconnectQtWidget
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
)

import mullvad_cli  # must provide get_lockdown_state() and set_lockdown_state(enabled: bool)


def main() -> int:
    app = QApplication(sys.argv)

    w = QWidget()
    w.setWindowTitle("Mullvad UI")
    w.resize(520, 300)

    layout = QVBoxLayout(w)

    title = QLabel("Mullvad UI")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setStyleSheet("font-size: 24px; font-weight: 600;")
    layout.addWidget(title)

    lockdown = LockdownQtWidget(w)
    layout.addWidget(lockdown)

    connect_disconnect = ConnectDisconnectQtWidget(w)
    layout.addWidget(connect_disconnect)    

    w.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
