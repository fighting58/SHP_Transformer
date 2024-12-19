from PySide6.QtWidgets import QApplication, QFileDialog, QWidget, QPushButton
from PySide6.QtCore import Qt, QSize, QRegularExpression, QFile, QTextStream
from PySide6.QtGui import QIcon, QPixmap, QRegularExpressionValidator, QCursor
import sys
from shp_convert import calculate_dxdy, calculate_length_and_bearing, adjust_shapefile_features
from main_ui import Ui_Form
import resources
from QCustomModals import QCustomModals
import os
import tempfile


class ShpConverter(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setFixedSize(480, 290)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 테두리 없는 윈도우 생성
        self.setAttribute(Qt.WA_TranslucentBackground)  # 투명 배경 설정
        self.setupUi(self)

        self.shp = None
        self.saveas = None        
        
        self.input_path1.setPlaceholderText("Shp 파일 입력")
        self.input_button1.icon_normal = QIcon(':/images/shapefile_dark.svg')
        self.input_button1.icon_hover = QIcon(':/images/shapefile_white.svg')
        self.input_button1.setToolTip("Shp파일 불러오기")
        self.input_button1.refresh()
        self.main_frame.setFixedSize(480, 290)
        self.round = 10

        # 좌표 입력란에 validator 설정
        regExp = QRegularExpression(r'^[0-9]*\.?[0-9]*$')
        validator = QRegularExpressionValidator(regExp)
        for lineedit in [self.px1, self.px2, self.py1, self.py2, self.qx1, self.qx2, self.qy1, self.qy2]:
            lineedit.setValidator(validator)

        # 파일 입력 및 실행버튼 클릭 시
        self.input_button1.clicked.connect(self.get_shp)
        self.btn_run.clicked.connect(self.run)
        self.titlebar.help_btn.clicked.connect(self.open_pdf)

        # 스타일 적용
        style_file = QFile(':/styles/styles.qss')
        if style_file.open(QFile.ReadOnly | QFile.Text):
            style_stream = QTextStream(style_file)
            self.setStyleSheet(style_stream.readAll())

    def get_shp(self):
        """ 파일 불러오기 """
        shp, _ = QFileDialog.getOpenFileName(self, caption="Select shp file", directory='', filter='shp file(*.shp)')
        if shp:
            self.input_path1.setText(shp)
            self.shp = shp
            self.saveas = shp.replace(".shp", "_converted.shp")
        else:
            self.shp = None
            self.input_path1.setText('')
    
    def show_modal(self, modal_type, **kargs):
        """ 메시지 송출 """
        default_settings = {'position': 'bottom-left', 'duration': 2000, 'closeIcon': ':/images/x.svg'}
        modal_collection = {'info':QCustomModals.InformationModal, 
                            'success':QCustomModals.SuccessModal, 
                            'error':QCustomModals.ErrorModal, 
                            'warning':QCustomModals.WarningModal, 
                            'custom':QCustomModals.CustomModal}
        if modal_type not in ['info', 'success', 'error', 'warning', 'custom']: modal_type = 'custom'

        for key, value in kargs.items():
            default_settings[key] = value    

        modal = modal_collection[modal_type](**default_settings)
        modal.show()


    def open_pdf(self):
        # 열고자 하는 PDF 파일의 경로
        pdf_path = QFile(":/help/SHP_Coordinate_Converter_helper.pdf")

        if not pdf_path.open(QFile.ReadOnly):
            print("Failed to open resource file")
            return

        # 임시 파일에 PDF 저장
        temp_dir = tempfile.gettempdir()
        temp_pdf_path = os.path.join(temp_dir, "SHP_Coordinate_Converter_helper.pdf")
        
        with open(temp_pdf_path, 'wb') as temp_file:
            temp_file.write(pdf_path.readAll())
        
        # PDF 파일을 기본 뷰어로 열기
        if sys.platform == "win32":  # Windows
            os.startfile(temp_pdf_path)
        elif sys.platform == "darwin":  # macOS
            os.system(f"open {temp_pdf_path}")
        else:  # Linux and others
            os.system(f"xdg-open {temp_pdf_path}")

    def run(self):
        # shp파일 입력했는지 확인
        if self.shp is None:
            self.show_modal("error", parent=self.main_frame, title="Input SHP File Required", description="Please enter a valid shp filename to proceed.")
            return            

        # 모든 좌표를 기입했는지 확인 및 변환
        try:
            l1_s = (float(self.py1.text()), float(self.px1.text()))
            l1_e = (float(self.py2.text()), float(self.px2.text()))
            l2_s = (float(self.qy1.text()), float(self.qx1.text()))
            l2_e = (float(self.qy2.text()), float(self.qx2.text()))
        except Exception as e:
            self.show_modal("error", parent=self.main_frame, title="Missing Input Fields", description="Please ensure that all fields are filled out before proceeding.")
            return

        # 변환량 계산
        r1, v1 = calculate_length_and_bearing(l1_s, l1_e) # 기준선의 거리 방위각
        r2, v2 = calculate_length_and_bearing(l2_s, l2_e) # 이동선의 거리 방위각

        translation = calculate_dxdy(l1_s, l2_s)  # x, y 이동량
        rotation_angle = v2 - v1 # 회전량
        scaling_factor = r2 / r1 # 축척계수
        rotation_origin = (l2_s[0], l2_s[1])  # 회전 기준점

        # 변환 실행
        try:
            adjust_shapefile_features(self.shp, self.saveas, translation, rotation_angle, scaling_factor, rotation_origin=rotation_origin)
            self.show_modal('success', parent=self.main_frame, title="Transform Success", description=f"Export: {self.saveas}")
        except Exception as e:
            self.show_modal("error", parent=self.main_frame, title="Transform Failed", description=f"{e}")

    # ==== 위젯 이동 관련 ===============
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # Get the position of the mouse relative to the window
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # Change mouse icon

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_flag:
            self.move(event.globalPos() - self.m_Position)  # Change window position
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
    # ==================================

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = ShpConverter()
    myWindow.show()

    sys.exit(app.exec_())