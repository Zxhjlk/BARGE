from PyQt5.QtWidgets import QApplication, QWidget
import sys

app = QApplication(sys.argv)
window = QWidget()
window.show

if __name__ == "__main__":
    app.exec()
    # Main launch of window
