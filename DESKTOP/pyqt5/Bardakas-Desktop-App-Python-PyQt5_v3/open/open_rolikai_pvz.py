from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import Bardakas_style_gray
from scaling import pt_points

class ImgRolikuPvz(QDialog, pt_points):
    def __init__(self):
        """mainWindow"""
        super().__init__()
        self.setWindowTitle('Rolikų pvz.')
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(int(100 / self.scale_factor), int(100 / self.scale_factor),
                         int(800 * self.scale_factor), int(600 * self.scale_factor))
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        Bardakas_style_gray.QDialogsheetstyle(self)

        self.settings = QSettings('Bardakas', 'Rolikai_pvz')
        # print(self.settings.fileName())
        try:
            self.resize(self.settings.value('window size'))
            self.move(self.settings.value('window position'))
        except:
            pass

        self.UI()
        self.show()

    def closeEvent(self, event):
        self.settings.setValue('window size', self.size())
        self.settings.setValue('window position', self.pos())

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        self.label1 = QLabel()
        self.label1.setText("Su sriegiu: ")
        self.label1.setFixedWidth(80)

        self.label2 = QLabel()
        self.label2.setText("Su šešiakampe\našim: ")
        self.label2.setFixedWidth(110)

        self.label3 = QLabel()
        self.label3.setText("Su ašim: ")
        self.label3.setFixedWidth(65)

        self.pixmap4 = QPixmap('img/su_sriegiu.jpg')
        self.pixmapscale4 = self.pixmap4.scaled(100, 90)
        self.label4 = QLabel()
        self.label4.setPixmap(self.pixmapscale4)
        self.label4.setFixedWidth(150)

        self.pixmap5 = QPixmap('img/su_s_asim.jpg')
        self.pixmapscale5 = self.pixmap5.scaled(100, 90)
        self.label5 = QLabel()
        self.label5.setPixmap(self.pixmapscale5)
        self.label5.setFixedWidth(150)

        self.pixmap6 = QPixmap('img/su_asim.jpg')
        self.pixmapscale6 = self.pixmap6.scaled(100, 90)
        self.label6 = QLabel()
        self.label6.setPixmap(self.pixmapscale6)
        self.label6.setFixedWidth(150)

        #######################################################################################
        self.label7 = QLabel()
        self.label7.setText("2xD5: ")

        self.label8 = QLabel()
        self.label8.setText("2xD5 toliau: ")

        self.label9 = QLabel()
        self.label9.setText("AT10: ")

        self.label13 = QLabel()
        self.label13.setText("PJ: ")

        self.label15 = QLabel()
        self.label15.setText("HABASIT: ")

        self.label17 = QLabel()
        self.label17.setText("2xŽvaigždė: ")

        self.pixmap10 = QPixmap('img/2xd5.jpg')
        self.pixmapscale10 = self.pixmap10.scaled(100, 90)
        self.label10 = QLabel()
        self.label10.setPixmap(self.pixmapscale10)
        self.label10.setFixedWidth(150)

        self.pixmap11 = QPixmap('img/2xd5_toliau.jpg')
        self.pixmapscale11 = self.pixmap11.scaled(100, 90)
        self.label11 = QLabel()
        self.label11.setPixmap(self.pixmapscale11)
        self.label11.setFixedWidth(150)

        self.pixmap12 = QPixmap('img/at10.jpg')
        self.pixmapscale12 = self.pixmap12.scaled(100, 90)
        self.label12 = QLabel()
        self.label12.setPixmap(self.pixmapscale12)
        self.label12.setFixedWidth(150)

        self.pixmap14 = QPixmap('img/pj.jpg')
        self.pixmapscale14 = self.pixmap14.scaled(100, 90)
        self.label14 = QLabel()
        self.label14.setPixmap(self.pixmapscale14)
        self.label14.setFixedWidth(150)

        self.pixmap16 = QPixmap('img/habasit.jpg')
        self.pixmapscale16 = self.pixmap16.scaled(100, 90)
        self.label16 = QLabel()
        self.label16.setPixmap(self.pixmapscale16)
        self.label16.setFixedWidth(150)

        self.pixmap18 = QPixmap('img/2xZvaigzde.jpg')
        self.pixmapscale18 = self.pixmap18.scaled(100, 90)
        self.label18 = QLabel()
        self.label18.setPixmap(self.pixmapscale18)
        self.label18.setFixedWidth(150)

    def layouts(self):
        self.mainLayout = QVBoxLayout()

        self.tvirtinimasPavLayout = QVBoxLayout()
        self.tvirtinimasLayout = QGridLayout()

        self.tipasPavLayout = QVBoxLayout()
        self.tipasLayout = QGridLayout()

        self.tvirtinimasPavLayout.addWidget(QLabel("Tvirtinimo pvz.:"), alignment=Qt.AlignCenter)
        self.tvirtinimasPavLayout.addWidget(QLabel(""), alignment=Qt.AlignCenter)

        self.tvirtinimasLayout.addWidget(self.label1, 0, 0, alignment=Qt.AlignTop)
        self.tvirtinimasLayout.addWidget(self.label4, 0, 1, alignment=Qt.AlignTop)

        self.tvirtinimasLayout.addWidget(self.label2, 0, 2, alignment=Qt.AlignTop)
        self.tvirtinimasLayout.addWidget(self.label5, 0, 3, alignment=Qt.AlignTop)

        self.tvirtinimasLayout.addWidget(self.label3, 0, 4, alignment=Qt.AlignTop)
        self.tvirtinimasLayout.addWidget(self.label6, 0, 5, alignment=Qt.AlignTop)

        #####################################################################################
        self.tipasPavLayout.addWidget(QLabel(""), alignment=Qt.AlignCenter)
        self.tipasPavLayout.addWidget(QLabel(""), alignment=Qt.AlignCenter)
        self.tipasPavLayout.addWidget(QLabel("Rolikų pvz.:"), alignment=Qt.AlignCenter)
        self.tipasPavLayout.addWidget(QLabel(""), alignment=Qt.AlignCenter)

        self.tipasLayout.addWidget(self.label7, 0, 0, alignment=Qt.AlignRight)
        self.tipasLayout.addWidget(self.label10, 0, 1, alignment=Qt.AlignTop)

        self.tipasLayout.addWidget(self.label8, 0, 2, alignment=Qt.AlignRight)
        self.tipasLayout.addWidget(self.label11, 0, 3, alignment=Qt.AlignTop)

        self.tipasLayout.addWidget(self.label9, 0, 4, alignment=Qt.AlignRight)
        self.tipasLayout.addWidget(self.label12, 0, 5, alignment=Qt.AlignTop)



        ######################################################################################
        self.tipasLayout.addWidget(self.label13, 1, 0, alignment=Qt.AlignRight)
        self.tipasLayout.addWidget(self.label14, 1, 1, alignment=Qt.AlignTop)

        self.tipasLayout.addWidget(self.label15, 1, 2, alignment=Qt.AlignRight)
        self.tipasLayout.addWidget(self.label16, 1, 3, alignment=Qt.AlignTop)

        self.tipasLayout.addWidget(self.label17, 1, 4, alignment=Qt.AlignRight)
        self.tipasLayout.addWidget(self.label18, 1, 5, alignment=Qt.AlignTop)

        ######################################################################################
        self.mainLayout.addLayout(self.tvirtinimasPavLayout, 1)
        self.mainLayout.addLayout(self.tvirtinimasLayout, 1)
        self.mainLayout.addLayout(self.tipasPavLayout, 1)
        self.mainLayout.addLayout(self.tipasLayout, 97)

        self.setLayout(self.mainLayout)

def main():
    import sys

    App = QApplication(sys.argv)
    window = ImgRolikuPvz()


    sys.exit(App.exec_())


if __name__ == '__main__':
    main()