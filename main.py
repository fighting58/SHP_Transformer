from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget
from PyQt5 import uic
import sys
from shp_transform import calculate_dxdy, calculate_length_and_bearing, adjust_shapefile_features

form_class = uic.loadUiType('main.ui')[0]

class MyCIF(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 
        self.saveas = ''

        self.input_button1.clicked.connect(self.get_shp)

    def get_shp(self):
        shp, _ = QFileDialog.getOpenFileName(self, caption="Select shp file", directory='', filter='shp file(*.shp)')
        print(shp)
        if shp:
            self.input_path1.setText(shp)
            self.saveas = shp.replace(".shp", "_transformed.shp")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyCIF()
    myWindow.show()

    sys.exit(app.exec_())