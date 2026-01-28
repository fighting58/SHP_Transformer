from PySide6.QtWidgets import QApplication, QFileDialog, QWidget, QPushButton, QLineEdit
from PySide6.QtCore import Qt, QSize, QRegularExpression, QFile, QTextStream
from PySide6.QtGui import QIcon, QPixmap, QRegularExpressionValidator, QCursor
import sys
from shp_convert import calculate_dxdy, calculate_length_and_bearing, adjust_shapefile_features
from main_ui import Ui_Form
import resources
from QCustomModals import QCustomModals
import os
import tempfile
import json

class ShpConverter(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setFixedSize(630, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 테두리 없는 윈도우 생성
        self.setAttribute(Qt.WA_TranslucentBackground)  # 투명 배경 설정
        self.setupUi(self)

        self.shp = None
        self.saveas = None  
        self.conv_file = None   
        self.conv_reverse  = False  # 역변환 여부
        self.encoding = 'cp949' 
        
        self.input_path1.setPlaceholderText("Shp 파일 입력")
        self.input_button1.icon_normal = QIcon(':/images/shapefile_dark.svg')
        self.input_button1.icon_hover = QIcon(':/images/shapefile_white.svg')
        self.input_button1.setToolTip("Shp파일 불러오기")
        self.input_button1.refresh()

        self.btn_conv_init.icon_normal = QIcon(':/images/file.svg')
        self.btn_conv_init.icon_hover = QIcon(':/images/file.svg')
        self.btn_conv_init.setToolTip("새로 작성")
        self.btn_conv_init.refresh()

        self.btn_conv_open.icon_normal = QIcon(':/images/folder-open.svg')
        self.btn_conv_open.icon_hover = QIcon(':/images/folder-open.svg')
        self.btn_conv_open.setToolTip("좌표변환 파일 불러오기")
        self.btn_conv_open.refresh()

        self.btn_conv_save.icon_normal = QIcon(':/images/save.svg')
        self.btn_conv_save.icon_hover = QIcon(':/images/save.svg')
        self.btn_conv_save.setToolTip("좌표변환 파일 저장")
        self.btn_conv_save.refresh()

        self.btn_conv_reverse.icon_normal = QIcon(':/images/arrow-right-arrow-left.svg')
        self.btn_conv_reverse.icon_hover = QIcon(':/images/arrow-right-arrow-left.svg')    
        self.btn_conv_reverse.setToolTip("역변환")
        self.btn_conv_reverse.refresh()

        self.encoding_cp949.setChecked(True)

        self.main_frame.setFixedSize(630, 400)
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

        self.btn_conv_init.clicked.connect(self.init_convert)  # shp 파일입력을 제외한 모든 라인에디트 내용 초기화
        self.btn_conv_open.clicked.connect(self.open_convert)  # 좌표변환 파일 읽고 변환값 입력
        self.btn_conv_save.clicked.connect(self.save_convert)  # 좌표변환 파일 저장
        self.btn_conv_reverse.clicked.connect(self.reverse_convert)  # 좌표변환 변환값 반전
        self.encoding_cp949.toggled.connect(self.on_encoding_change)
        self.encoding_utf8.toggled.connect(self.on_encoding_change)

        # 라인에디트 탭 오더 적용
        editable_lineedits = [self.lineedit_saup_name, self.lineedit_detail, self.px1, self.py1, self.qx1, self.qy1, self.px2, self.py2, self.qx2, self.qy2]        
        for current, next_widget in zip(editable_lineedits, editable_lineedits[1:]):
            self.setTabOrder(current, next_widget)

        # 라인에디트 포커스 이동 적용(엔터 입력시)
        for le in self.findChildren(QLineEdit):
            if le.objectName() != "input_path1":   # shp 파일 입력 제외
                le.returnPressed.connect(self.focusNextChild)

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

    def on_encoding_change(self):
        """ 파일 인코딩 변경 """
        if self.encoding_cp949.isChecked():
            self.encoding = 'cp949'
        else:
            self.encoding = 'utf-8'

    def init_convert(self):
        """ 좌표변환값 초기화 """   
        self.conv_file = None
        self.conv_reverse = False
        for line_edit in self.findChildren(QLineEdit):
            if line_edit.objectName() != "input_path1":
                line_edit.clear()

    def open_convert(self):
        """ 좌표변환 파일 읽고 변환값 입력 """
        conv_file, _ = QFileDialog.getOpenFileName(self, caption="Select Conversion File", directory='', filter='*.json')
        if conv_file:
            self.conv_file = conv_file
            self.conv_reverse = False
            with open(conv_file, "r") as f:
                dict_convert = json.load(f)
                self.lineedit_saup_name.setText(dict_convert["saup_name"])
                self.lineedit_detail.setText(dict_convert["detail"])
                self.px1.setText(dict_convert["px1"])
                self.py1.setText(dict_convert["py1"])
                self.qx1.setText(dict_convert["qx1"])
                self.qy1.setText(dict_convert["qy1"])
                self.px2.setText(dict_convert["px2"])
                self.py2.setText(dict_convert["py2"])
                self.qx2.setText(dict_convert["qx2"])                
                self.qy2.setText(dict_convert["qy2"])   

    def save_convert(self):
        """ 좌표변환 파일 저장 """
        # 데이터 유효성 검사
        valid_check = (self.lineedit_saup_name.text().strip() != "") and (self.lineedit_detail.text().strip() != "") \
                      and (self.px1.text() != "") and (self.py1.text() != "") and (self.qx1.text() != "") and (self.qy1.text() != "") \
                      and (self.px2.text() != "") and (self.py2.text() != "") and (self.qx2.text() != "") and (self.qy2.text() != "")
        
        if valid_check:
            dict_convert = {
                "saup_name": self.lineedit_saup_name.text().strip(),
                "detail": self.lineedit_detail.text().strip(),
                "px1": self.px1.text(),
                "py1": self.py1.text(),
                "qx1": self.qx1.text(),
                "qy1": self.qy1.text(),
                "px2": self.px2.text(),
                "py2": self.py2.text(),
                "qx2": self.qx2.text(),
                "qy2": self.qy2.text()
            }

            saveas, _ = QFileDialog.getSaveFileName(self, caption="Save Convert File", directory='', filter='*.json')

            with open(saveas, "w") as f:
                json.dump(dict_convert, f)        
                self.show_modal('success', parent=self.main_frame, title="Save Success", description=f"Saved to {saveas}")

            self.conv_file = saveas
            self.conv_reverse = False
        else:
            self.show_modal("error", parent=self.main_frame, title="Missing Input Fields", description="Please ensure that all fields are filled out before proceeding.")


    def reverse_convert(self):
        """ 좌표변환 변환값 반전 """        
        px1, py1 = self.px1.text(), self.py1.text()
        qx1, qy1 = self.qx1.text(), self.qy1.text()
        px2, py2 = self.px2.text(), self.py2.text()
        qx2, qy2 = self.qx2.text(), self.qy2.text()

        self.px1.setText(qx1)
        self.py1.setText(qy1)
        self.qx1.setText(px1)
        self.qy1.setText(py1)
        self.px2.setText(qx2)
        self.py2.setText(qy2)
        self.qx2.setText(px2)
        self.qy2.setText(py2)

        self.conv_reverse = not self.conv_reverse
        if self.conv_reverse and self.conv_file is not None:
            self.lineedit_saup_name.setText(self.lineedit_saup_name.text() + " (Reverse)")
            self.lineedit_saup_name.setStyleSheet("color: #ff0000")
        else:
            self.lineedit_saup_name.setText(self.lineedit_saup_name.text().replace(" (Reverse)", ""))
            self.lineedit_saup_name.setStyleSheet("color: #88f3a8")
    
    def focus_next_lineedit(self):
        self.focusNextChild()

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
            adjust_shapefile_features(self.shp, self.saveas, translation, rotation_angle, scaling_factor, rotation_origin=rotation_origin, encoding=self.encoding)
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