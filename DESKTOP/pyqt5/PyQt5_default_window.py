from PyQt5.QtWidgets import *



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("BARDAKAS")
        self.setGeometry(100, 100, 1200, 720)


def main():
    import sys
    App = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(App.exec_())

if __name__ == '__main__':
    main()