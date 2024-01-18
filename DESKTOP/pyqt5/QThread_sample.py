import sys
import time
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel


# Define a custom QThread class
class WorkerThread(QThread):
    finished_signal = pyqtSignal(str)  # Signal to be emitted when the task is finished

    # Override the run method with the task to be executed in the thread
    def run(self):
        for i in range(5):
            time.sleep(1)  # Simulate a time-consuming task
            self.finished_signal.emit(f"Task iteration {i + 1} completed.")


# Define the main application window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QThread Example")
        self.setGeometry(100, 100, 300, 200)

        # Create the main layout
        layout = QVBoxLayout()

        # Create a button and connect it to the start_task method
        self.button = QPushButton("Start Task")
        self.button.clicked.connect(self.start_task)
        layout.addWidget(self.button)

        # Create a label to display the status
        self.status_label = QLabel("Status: Waiting for task to start...")
        layout.addWidget(self.status_label)

        # Set the layout as the central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Method to start the task in a separate thread
    def start_task(self):
        self.thread = WorkerThread()  # Create an instance of the custom thread class
        self.thread.finished_signal.connect(self.update_status)  # Connect signal to method
        self.thread.start()  # Start the thread
        self.status_label.setText("Status: Task is running...")  # Update the status label

    # Method to update the status label when the task progresses
    def update_status(self, message):
        self.status_label.setText(f"Status: {message}")


# Main application entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create the application instance
    window = MainWindow()  # Create the main window instance
    window.show()  # Display the window
    sys.exit(app.exec_())  # Start the application event loop
