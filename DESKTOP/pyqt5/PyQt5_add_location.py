def OpenFolderDialog(self):
    """get folder dir"""
    directory = str(QtWidgets.QFileDialog.getExistingDirectory())
    self.locEntry.setText('{}'.format(directory))


def OpenFileDialog(self):
    """getOpenFileName creates tuples and we need just dir, get file dir"""
    (directory, fileType) = QtWidgets.QFileDialog.getOpenFileName()
    self.ListEntry.setText('{}'.format(directory))

