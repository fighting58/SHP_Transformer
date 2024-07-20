from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget
from PyQt5 import uic
import sys
from shp_transform import calculate_dxdy, calculate_length_and_bearing, adjust_shapefile_features

form_class = uic.loadUiType('main.ui')[0]

class ShpTransformer(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 
        self.shp = None
        self.saveas = None

        self.input_button1.clicked.connect(self.get_shp)
        self.btn_run.clicked.connect(self.run)

    def get_shp(self):
        shp, _ = QFileDialog.getOpenFileName(self, caption="Select shp file", directory='', filter='shp file(*.shp)')
        if shp:
            self.input_path1.setText(shp)
            self.shp = shp
            self.saveas = shp.replace(".shp", "_transformed.shp")
    
    def run(self):
        l1_s = (float(self.py1.text()), float(self.px1.text()))
        l1_e = (float(self.py2.text()), float(self.px2.text()))
        l2_s = (float(self.qy1.text()), float(self.qx1.text()))
        l2_e = (float(self.qy2.text()), float(self.qx2.text()))

        dxdy = calculate_dxdy(l1_s, l2_s)
        r1, v1 = calculate_length_and_bearing(l1_s, l1_e)
        r2, v2 = calculate_length_and_bearing(l2_s, l2_e)

        s = r2 / r1
        dv = v2 - v1

        translation = dxdy  # x 방향으로 10만큼, y 방향으로 20만큼 이동
        rotation_angle = dv # 45도 회전
        scaling_factor = s # 1.5배 축척
        rotation_origin = (l2_s[0], l2_s[1])

        adjust_shapefile_features(self.shp, self.saveas, translation, rotation_angle, scaling_factor, rotation_origin=rotation_origin)

    
"""
    l1_s = Point(217351.37, 505549.82)
    l1_e = Point(216828.55, 507359.74)
    l2_s = Point(219991.27, 505193.11)
    l2_e = Point(219657.02, 507186.06)
"""



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = ShpTransformer()
    myWindow.show()

    sys.exit(app.exec_())