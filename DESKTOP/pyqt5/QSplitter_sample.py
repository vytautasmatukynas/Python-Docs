import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QTextEdit

app = QApplication(sys.argv)

main_window = QMainWindow()
splitter = QSplitter(main_window)
left_widget = QTextEdit("Left Pane")
right_widget = QTextEdit("Right Pane")

splitter.addWidget(left_widget)
splitter.addWidget(right_widget)

main_window.setCentralWidget(splitter)
main_window.show()

sys.exit(app.exec_())
