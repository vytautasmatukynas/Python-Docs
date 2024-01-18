__version__ = '1.0'

def updateInfoOnStart(self):
    """version check"""
    try:
        # Version file link
        response = requests.get(
            'version check link')
        data = response.text

        if float(data) > float(__version__):
            # self.msg = QMessageBox.information(self, "UPDATE", "Bardakas 1.3.0")
            msg = QMessageBox()
            msg.setWindowTitle("UPDATE MANAGER")
            msg.setText('Update! Version {} to {}.'.format(__version__, data))
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon('icons/icon.ico'))
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

            if (x == QMessageBox.Yes):
                # Donwload file link
                webbrowser.open_new_tab(
                    'download link')
                self.close()

            else:
                pass

        else:
            pass

    except:
        msg = QMessageBox()
        msg.setWindowTitle("ERROR...")
        msg.setText("Error, check your internet connection or\n"
                    "contact system administrator.")
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QIcon('icons/icon.ico'))

        Bardakas_style_gray.msgsheetstyle(msg)

        x = msg.exec_()