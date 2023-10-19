from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
import sys
class MainWindow(QMainWindow):
      def __init__(self):
            super(MainWindow, self).__init__()
            self.setWindowTitle("Barge Kanban")            
            layout = QVBoxLayout()
            widget = QWidget()
            widget.setLayout(layout)
            self.setCentralWidget(widget)

if __name__ == "__main__":
      app = QApplication(sys.argv)
      window = MainWindow()
      window.show()
      app.exec()
      #Main launch of window
