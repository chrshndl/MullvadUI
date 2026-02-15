import sys

from PySide6.QtCore import Qt, QEvent, QPoint, QTimer, QSettings
from PySide6.QtGui import QAction, QCursor, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMenu,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from lockdown_widget import LockdownQtWidget
from connect_disconnect import ConnectDisconnectQtWidget

import mullvad_cli  # keep import for side effects / future use


APP_ORG = "MullvadUI"
APP_NAME = "MullvadUI"


def clamp(n: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, n))


def compute_bottom_right_pos(window: QWidget, margin: int = 12) -> QPoint:
    cursor_pos = QCursor.pos()
    screen = QApplication.screenAt(cursor_pos) or QApplication.primaryScreen()
    if not screen:
        return QPoint(50, 50)

    avail = screen.availableGeometry()

    w = window.width()
    h = window.height()

    x = avail.x() + avail.width() - w - margin
    y = avail.y() + avail.height() - h - margin

    x = clamp(x, avail.x() + margin, avail.x() + avail.width() - w - margin)
    y = clamp(y, avail.y() + margin, avail.y() + avail.height() - h - margin)
    return QPoint(x, y)


class TrayWindow(QWidget):
    """
    Wayland-safe: normal (movable) tool window, hides on focus loss.
    We cannot reliably force pixel-perfect placement on Wayland, so we:
      - try bottom-right as best effort
      - remember last position (user drags it once)
    """
    def __init__(self) -> None:
        super().__init__()

        # Keep it "utility-like" but STILL movable (no frameless!)
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)

        self.setWindowTitle("Mullvad UI")
        self.setFixedSize(260, 420)

        # Hide when losing focus (tray-popup-ish UX)
        self.installEventFilter(self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        title = QLabel("Mullvad UI")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: 600;")
        layout.addWidget(title)

        layout.addWidget(LockdownQtWidget(self))
        layout.addWidget(ConnectDisconnectQtWidget(self))
        layout.addStretch(1)

        self._settings = QSettings(APP_ORG, APP_NAME)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowDeactivate:
            self.hide()
        return super().eventFilter(obj, event)

    def moveEvent(self, event):
        # Persist position whenever user moves it
        self._settings.setValue("window_pos", self.pos())
        return super().moveEvent(event)

    def show_best_effort(self) -> None:
        # 1) If we have a saved position, prefer it
        saved = self._settings.value("window_pos")
        if isinstance(saved, QPoint):
            target = saved
        else:
            target = compute_bottom_right_pos(self)

        # 2) Best effort move BEFORE show
        self.move(target)
        self.show()
        self.raise_()
        self.activateWindow()

        # 3) Best effort move AFTER show (Wayland timing)
        def apply_pos():
            # Some compositors only apply after mapping
            self.move(target)

        QTimer.singleShot(0, apply_pos)
        QTimer.singleShot(50, apply_pos)
        QTimer.singleShot(150, apply_pos)


def setup_tray(app: QApplication, window: TrayWindow) -> QSystemTrayIcon:
    tray = QSystemTrayIcon(QIcon.fromTheme("network-vpn"), parent=app)
    tray.setToolTip("Mullvad UI")

    menu = QMenu()
    act_toggle = QAction("Show/Hide", menu)
    act_quit = QAction("Quit", menu)

    def toggle_window():
        if window.isVisible():
            window.hide()
        else:
            window.show_best_effort()

    def quit_app():
        tray.hide()
        app.quit()

    act_toggle.triggered.connect(toggle_window)
    act_quit.triggered.connect(quit_app)

    menu.addAction(act_toggle)
    menu.addSeparator()
    menu.addAction(act_quit)

    tray.setContextMenu(menu)

    # Left-click toggles the window (no QMenu popup => avoids Wayland grabbing popup error)
    tray.activated.connect(lambda reason: toggle_window() if reason == QSystemTrayIcon.Trigger else None)

    tray.show()
    return tray


def main() -> int:
    app = QApplication(sys.argv)
    QApplication.setOrganizationName(APP_ORG)
    QApplication.setApplicationName(APP_NAME)

    window = TrayWindow()
    window.hide()

    setup_tray(app, window)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
