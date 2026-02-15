import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt

def main() -> int:
    app = QApplication(sys.argv)
    
    w=QWidget()
    w.setWindowTitle("Mullvad UI")
    w.resize(520,300)

    layout = QVBoxLayout(w)

    title = QLabel("Hello from first version")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setStyleSheet("font-size: 24px; font-weight: 600;")
    layout.addWidget(title)

    btn = QPushButton("Click")
    btn.clicked.connect(lambda: title.setText("Clicked"))
    layout.addWidget(btn)

    w.show()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())