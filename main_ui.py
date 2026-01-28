# -*- coding: utf-8 -*-

from PySide6 import QtCore, QtGui, QtWidgets

class IconChangingButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self._icon_hover=QtGui.QIcon()
        self._icon_normal=QtGui.QIcon()
 
    @property
    def icon_normal(self):
        return self._icon_normal

    @icon_normal.setter
    def icon_normal(self, icon):
        self._icon_normal = icon
        self.refresh()
 
    @property
    def icon_hover(self):
        return self._icon_hover

    @icon_hover.setter
    def icon_hover(self, icon):
        self._icon_hover = icon

    def refresh(self):
        if self._icon_normal:
            self.setIcon(self._icon_normal)  
        else:
            self.setIcon(QtGui.QIcon())          
        self.setIconSize(QtCore.QSize(24,24))

    def enterEvent(self, event):
        self.setIcon(self.icon_hover)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self.icon_normal)
        super().leaveEvent(event)

class CustomTitleBar(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        title_bar_layout = QtWidgets.QHBoxLayout(self)
        title_bar_layout.setContentsMargins(1,1,1,1)
        title_bar_layout.setSpacing(2)
        self.title = QtWidgets.QLabel(f"{self.__class__.__name__}", self)
        self.title.setObjectName("title")
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.help_btn = QtWidgets.QToolButton(self)
        self.help_btn.setObjectName('helpbutton')
        help_icon = self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_TitleBarContextHelpButton)
        self.help_btn.setIcon(help_icon)
        self.help_btn.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.help_btn.setFixedSize(QtCore.QSize(20,20))
        self.close_btn = QtWidgets.QToolButton(self)
        self.close_btn.setObjectName('closebutton')
        close_icon = self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_TitleBarCloseButton)
        self.close_btn.setIcon(close_icon)
        self.close_btn.clicked.connect(self.window().close)
        self.close_btn.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.close_btn.setFixedSize(QtCore.QSize(20,20))
        self.close_btn.setToolTip("Close Window")
        title_bar_layout.addWidget(self.title)
        title_bar_layout.addWidget(self.help_btn)
        title_bar_layout.addWidget(self.close_btn)

        self.set_title(parent)

    def set_title(self, parent):
        if title := parent.windowTitle():
            self.title.setText(title)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.resize(600, 400)
        self.main_layout = QtWidgets.QHBoxLayout(Form)
        self.main_layout.setObjectName("main_layout")
        self.main_frame = QtWidgets.QFrame(Form)
        self.main_frame.setObjectName("main_frame")
        self.main_frame_layout = QtWidgets.QVBoxLayout(self.main_frame)
        self.main_frame_layout.setObjectName("main_frame_layout")
        self.main_frame_layout.setContentsMargins(20,10,20,10)
        self.main_frame_layout.setSpacing(0)

        # 타이틀바 설정 ========================================
        self.titlebar = CustomTitleBar(Form)
        self.titlebar.setObjectName("titlebar")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        
        # 좌표변환 속성파일 관리 관련 레이아웃 =====================
        self.convert_manager_frame = QtWidgets.QFrame(self.main_frame)
        self.convert_manager_frame.setObjectName("convert_manager_frame")
        self.convert_manager_layout = QtWidgets.QGridLayout(self.convert_manager_frame)
        self.convert_manager_layout.setObjectName("convert_manager_layout")
        self.convert_manager_layout.setSpacing(5)
        # 좌표변환 속성파일 관리 위젯 설정
        self.label_saup_name = QtWidgets.QLabel(self.convert_manager_frame)
        self.label_saup_name.setObjectName("label_saup_name")
        self.lineedit_saup_name = QtWidgets.QLineEdit(self.convert_manager_frame)
        self.lineedit_saup_name.setObjectName("lineedit_saup_name")
        self.label_detail = QtWidgets.QLabel(self.convert_manager_frame)
        self.label_detail.setObjectName("label_detail")
        self.lineedit_detail = QtWidgets.QLineEdit(self.convert_manager_frame)
        self.lineedit_detail.setObjectName("lineedit_detail")
        self.btn_conv_init = IconChangingButton(self.convert_manager_frame)  # 좌표변환값 초기화
        self.btn_conv_init.setObjectName("btn_conv_init")
        self.btn_conv_init.setMaximumWidth(30)
        self.btn_conv_open = IconChangingButton(self.convert_manager_frame)  # 좌표변환값 호출
        self.btn_conv_open.setObjectName("btn_conv_open")  
        self.btn_conv_open.setMaximumWidth(30)
        self.btn_conv_save = IconChangingButton(self.convert_manager_frame)  # 좌표변환값 저장
        self.btn_conv_save.setObjectName("btn_conv_save") 
        self.btn_conv_save.setMaximumWidth(30)
        self.btn_conv_reverse = IconChangingButton(self.convert_manager_frame)  # 좌표 역변환
        self.btn_conv_reverse.setObjectName("btn_conv_reverse")
        self.btn_conv_reverse.setMaximumWidth(30)
        # 좌표변환 속성파일 관리 레이아웃 구성
        self.convert_manager_layout.addWidget(self.label_saup_name, 0, 0, 1, 1)
        self.convert_manager_layout.addWidget(self.lineedit_saup_name, 0, 2, 1, 1)
        self.convert_manager_layout.addWidget(self.label_detail, 1, 0, 1, 1)
        self.convert_manager_layout.addWidget(self.lineedit_detail, 1, 2, 1, 1)        
        self.convert_manager_layout.addWidget(self.btn_conv_init, 0, 3, 2, 1)
        self.convert_manager_layout.addWidget(self.btn_conv_open, 0, 4, 2, 1)
        self.convert_manager_layout.addWidget(self.btn_conv_save, 0, 5, 2, 1)
        self.convert_manager_layout.addWidget(self.btn_conv_reverse, 0, 6, 2, 1)
        self.convert_manager_frame.setLayout(self.convert_manager_layout)

        # 이동기준점 입력 그룹박스 및 그룹박스 레이아웃 =========================
        self.coordinate_groupbox = QtWidgets.QGroupBox(self.main_frame)
        self.coordinate_groupbox.setObjectName("coordinate_groupbox")
        self.coordinate_groupbox.setMinimumHeight(120)
        self.coordinate_groupbox_layout = QtWidgets.QGridLayout(self.coordinate_groupbox)
        self.coordinate_groupbox_layout.setObjectName("gridLayout")
        # 그룹박스 내 widget 설정
        self.label_x1 = QtWidgets.QLabel(self.coordinate_groupbox)
        self.label_x1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_x1.setObjectName("label")
        self.label_y1 = QtWidgets.QLabel(self.coordinate_groupbox)
        self.label_y1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_y1.setObjectName("label_y1")
        self.label_x2 = QtWidgets.QLabel(self.coordinate_groupbox)
        self.label_x2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_x2.setObjectName("label_x2")
        self.label_y2 = QtWidgets.QLabel(self.coordinate_groupbox)
        self.label_y2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_y2.setObjectName("label_y2")
        self.label_start = QtWidgets.QLabel(self.coordinate_groupbox)
        self.label_start.setObjectName("label_start")
        self.label_start.setAlignment(QtCore.Qt.AlignCenter)    
        self.px1 = QtWidgets.QLineEdit(self.coordinate_groupbox)
        self.px1.setObjectName("px1")
        self.py1 = QtWidgets.QLineEdit(self.coordinate_groupbox)
        self.py1.setObjectName("py1")
        self.label_arrow1 = QtWidgets.QLabel(self.coordinate_groupbox)
        self.label_arrow1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_arrow1.setObjectName("label_arrow1")
        self.qx1 = QtWidgets.QLineEdit(self.coordinate_groupbox)
        self.qx1.setObjectName("qx1")
        self.qy1 = QtWidgets.QLineEdit(self.coordinate_groupbox)
        self.qy1.setObjectName("qy1")
        self.label_end = QtWidgets.QLabel(self.coordinate_groupbox)
        self.label_end.setObjectName("label_end")
        self.label_end.setAlignment(QtCore.Qt.AlignCenter)
        self.px2 = QtWidgets.QLineEdit(self.coordinate_groupbox)
        self.px2.setObjectName("px2")
        self.py2 = QtWidgets.QLineEdit(self.coordinate_groupbox)
        self.py2.setObjectName("py2")
        self.label_arrow2 = QtWidgets.QLabel(self.coordinate_groupbox)
        self.label_arrow2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_arrow2.setObjectName("label_arrow2")
        self.qx2 = QtWidgets.QLineEdit(self.coordinate_groupbox)
        self.qx2.setObjectName("qx2")
        self.qy2 = QtWidgets.QLineEdit(self.coordinate_groupbox)
        self.qy2.setObjectName("qy2")
        # 그룹박스 레이아웃 구성
        self.coordinate_groupbox_layout.addWidget(self.label_x1, 0, 1, 1, 1)
        self.coordinate_groupbox_layout.addWidget(self.label_y1, 0, 2, 1, 1)
        self.coordinate_groupbox_layout.addWidget(self.label_x2, 0, 4, 1, 1)
        self.coordinate_groupbox_layout.addWidget(self.label_y2, 0, 5, 1, 1)
        self.coordinate_groupbox_layout.addWidget(self.label_start, 1, 0, 1, 1)
        self.coordinate_groupbox_layout.addWidget(self.px1, 1, 1, 1, 1)
        self.coordinate_groupbox_layout.addWidget(self.py1, 1, 2, 1, 1)
        self.coordinate_groupbox_layout.addWidget(self.label_arrow1, 1, 3, 1, 1)
        self.coordinate_groupbox_layout.addWidget(self.qx1, 1, 4, 1, 1)
        self.coordinate_groupbox_layout.addWidget(self.qy1, 1, 5, 1, 1)
        self.coordinate_groupbox_layout.addWidget(self.label_end, 2, 0, 1, 1)
        self.coordinate_groupbox_layout.addWidget(self.px2, 2, 1, 1, 1)
        self.coordinate_groupbox_layout.addWidget(self.py2, 2, 2, 1, 1)
        self.coordinate_groupbox_layout.addWidget(self.label_arrow2, 2, 3, 1, 1)
        self.coordinate_groupbox_layout.addWidget(self.qx2, 2, 4, 1, 1)
        self.coordinate_groupbox_layout.addWidget(self.qy2, 2, 5, 1, 1)

        # 파일 입력 프레임 및 프레임 레이아웃 ===========================
        self.fileinput_frame = QtWidgets.QFrame(self.main_frame)
        self.fileinput_frame.setObjectName("frame")
        self.fileinput_layout = QtWidgets.QHBoxLayout(self.fileinput_frame)
        self.fileinput_layout.setObjectName("fileinput_layout")
        self.fileinput_layout.setContentsMargins(0,0,0,0)
        # 변환 전 shp 파일 입력 필드
        self.input_button1 = IconChangingButton(self.fileinput_frame)
        self.input_button1.setObjectName("input_button1")
        self.input_button1.setMaximumWidth(40)
        self.input_path1 = QtWidgets.QLineEdit(self.fileinput_frame)
        self.input_path1.setReadOnly(True)
        self.input_path1.setObjectName("input_path1")
        # 파일입력 레이아웃 구성
        self.fileinput_layout.addWidget(self.input_button1)
        self.fileinput_layout.addWidget(self.input_path1)

        # encoding 프레임 및 레이아웃 ========================
        self.encoding_frame = QtWidgets.QFrame(self.main_frame)
        self.encoding_frame.setObjectName("encoding_frame")
        self.encoding_layout = QtWidgets.QHBoxLayout()
        self.encoding_layout.setObjectName("encoding_layout")
        self.encoding_layout.setContentsMargins(0,0,0,0)
        self.encoding_layout.setSpacing(20)
        self.label_encoding = QtWidgets.QLabel(self.fileinput_frame)
        self.label_encoding.setObjectName("label_encoding")
        self.encoding_cp949 = QtWidgets.QRadioButton(self.fileinput_frame)
        self.encoding_cp949.setObjectName("encoding_cp949")
        self.encoding_utf8 = QtWidgets.QRadioButton(self.fileinput_frame)
        self.encoding_utf8.setObjectName("encoding_utf8")
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)        
        self.encoding_layout.addItem(spacerItem2)
        self.encoding_layout.addWidget(self.label_encoding)
        self.encoding_layout.addWidget(self.encoding_cp949)
        self.encoding_layout.addWidget(self.encoding_utf8)
        self.encoding_frame.setLayout(self.encoding_layout)

        # 실행 프레임 및 프레임 레이아웃 ======================
        self.execute_frame = QtWidgets.QFrame(self.main_frame)
        self.execute_frame.setObjectName("execute_frame")
        self.execute_frame_layout = QtWidgets.QHBoxLayout(self.execute_frame)
        self.execute_frame_layout.setObjectName("execute_frame_layout")

        # H스페이스바 및 실행버튼
        spacerItem1 = QtWidgets.QSpacerItem(514, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.btn_run = QtWidgets.QPushButton(self.execute_frame)
        self.btn_run.setObjectName("btn_run")

        self.execute_frame_layout.addItem(spacerItem1)
        self.execute_frame_layout.addWidget(self.btn_run)

        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        spacerItem4 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        spacerItem5 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        # 메인 프레임 레이아웃 구성
        self.main_frame_layout.addWidget(self.titlebar)
        self.main_frame_layout.addItem(spacerItem)
        self.main_frame_layout.addWidget(self.convert_manager_frame)
        self.main_frame_layout.addItem(spacerItem3)
        self.main_frame_layout.addWidget(self.coordinate_groupbox)
        self.main_frame_layout.addItem(spacerItem4)
        self.main_frame_layout.addWidget(self.fileinput_frame)
        self.main_frame_layout.addWidget(self.encoding_frame)
        self.main_frame_layout.addItem(spacerItem5)
        self.main_frame_layout.addWidget(self.execute_frame)

        self.main_layout.addWidget(self.main_frame)               
        self.main_layout.setContentsMargins(0,0,0,0)

        self.retranslateUi(Form)
        self.titlebar.set_title(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "SHP Coordinate Converter"))
        self.label_saup_name.setText(_translate("Form", "사 업 명"))
        self.label_detail.setText(_translate("Form", "상세 설명"))
        self.coordinate_groupbox.setTitle(_translate("Form", "이동 기준점 입력"))
        self.label_arrow1.setText(_translate("Form", "⇒"))
        self.label_arrow2.setText(_translate("Form", "⇒"))        
        self.label_start.setText(_translate("Form", "시작점"))
        self.label_end.setText(_translate("Form", "끝  점"))  
        self.label_x1.setText(_translate("Form", "X"))      
        self.label_y1.setText(_translate("Form", "Y"))
        self.label_y2.setText(_translate("Form", "Y"))
        self.label_x2.setText(_translate("Form", "X"))        
        self.btn_run.setText(_translate("Form", "변환 실행"))
        self.label_encoding.setText(_translate("Form", "인코딩: "))
        self.encoding_cp949.setText(_translate("Form", "cp949"))
        self.encoding_utf8.setText(_translate("Form", "utf-8")) 

