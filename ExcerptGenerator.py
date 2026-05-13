from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QColorDialog, QFontDialog, QFrame, QFileDialog)
from PyQt6.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt6.QtCore import Qt, QRect

class ExcerptDialog(QDialog):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.original_text = text
        self.bg_color = QColor("#ffffff")
        self.text_color = QColor("#2c3e50")
        self.font = QFont("NanumMyeongjo", 20)
        if not self.font.exactMatch():
            self.font.setFamily("Batang")

        self.initUI()

    def initUI(self):
        #미리보기
        self.setWindowTitle("발췌")
        self.setFixedSize(500, 650)
        layout = QVBoxLayout(self)

        self.preview_label = QLabel()
        self.preview_label.setFixedSize(400, 400)
        self.preview_label.setStyleSheet("border: 1px solid #ccc;")
        layout.addWidget(self.preview_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # 설정 도구
        tools = QHBoxLayout()
        btn_bg = QPushButton("배경색")
        btn_bg.clicked.connect(self.choose_bg_color)

        btn_font = QPushButton("폰트/크기")
        btn_font.clicked.connect(self.choose_font)

        tools.addWidget(btn_bg)
        tools.addWidget(btn_font)
        layout.addLayout(tools)

        #저장
        btn_save = QPushButton("저장하기")
        btn_save.setFixedHeight(50)
        btn_save.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold")
        btn_save.clicked.connect(self.save_image)
        layout.addWidget(btn_save)

        self.update_preview()

    def update_preview(self):
        # 1. 고해상도 캔버스 생성
        self.final_image = QImage(1080, 1080, QImage.Format.Format_ARGB32)
        self.final_image.fill(self.bg_color)

        # 2. 페인터 시작
        painter = QPainter(self.final_image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing) # 텍스트 안티앨리어싱 추가

        if isinstance(self.font, QFont):
            painter.setFont(self.font)
        else:
            self.font = QFont("Batang", 20)
            painter.setFont(self.font)
            
        painter.setPen(self.text_color)

        # 4. 텍스트 영역 계산 및 그리기
        margin = 150
        rect = QRect(margin, margin, 1080 - (margin * 2), 1080 - (margin * 2))
        
        # 인용구 스타일로 텍스트 구성
        display_text = f"{self.original_text}"
        painter.drawText(
            rect, 
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter | Qt.TextFlag.TextWordWrap, 
            display_text
        )

        # 5. 페인터 종료
        painter.end()

        # 6. 미리보기 업데이트
        pixmap = QPixmap.fromImage(self.final_image.scaled(
            400, 400, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        ))
        self.preview_label.setPixmap(pixmap)
 
    def choose_bg_color(self):
        color = QColorDialog.getColor(self.bg_color,self)
        if color.isValid():
            self.bg_color = color
            self.update_preview()

    def choose_font(self):
        ok, font = QFontDialog.getFont(self.font, self)
        
        if ok: 
            self.font = font
            self.update_preview()   

    def save_image(self):
        path, _ = QFileDialog.getSaveFileName(self, "이미지 저장", "발췌_Bread.png", "PNG Files (*.png)")
        if path:
            self.final_image.save(path)
            self.accept()