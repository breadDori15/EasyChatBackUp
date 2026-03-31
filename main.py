import sys
import re
from PyQt6.QtWidgets import (QApplication, QMainWindow, QSplitter, QTextEdit, 
                             QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette
from bs4 import BeautifulSoup
from ColorPalette import ColorPaletteDialog

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    #프로그램 UI 설정
    def initUI(self):
        self.setWindowTitle('편집기 프로토타입')
        self.setGeometry(100, 100, 1000, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        header = QLabel("[왼쪽] 텍스트 입력 및 붙여넣기 [오른쪽] HTML 소스코드 실시간 확인")
        header.setFixedHeight(30)
        layout.addWidget(header)
        
        #body
        splitter = QSplitter(Qt.Orientation.Horizontal)

        #body.left
        self.left_editor = QTextEdit()
        self.left_editor.setAcceptRichText(True)
        self.left_editor.setPlaceholderText("여기에 내용을 입력")

        self.left_editor.textChanged.connect(self.update_html_source)
        
        #body.right
        self.right_editor = QTextEdit()
        self.right_editor.setReadOnly(True)
        self.right_editor.setStyleSheet("background-color: #2b2b2b; color: #a9b7c6; font-family: Consolas, monospace;")
        self.right_editor.setPlaceholderText("HTML 소스는 여기에 표시")

        splitter.addWidget(self.left_editor)
        splitter.addWidget(self.right_editor)
        splitter.setStretchFactor(0,1)
        splitter.setStretchFactor(1,1)

        layout.addWidget(splitter)

        #tool_box
        toolbar_widget = QWidget()
        toolbar_widget.setFixedHeight(60)
        toolbar_layout = QHBoxLayout(toolbar_widget)
        toolbar_layout.setContentsMargins(10, 0, 10, 0)

        self.btn_extract_colors = QPushButton("텍스트 색상 추출")
        self.btn_extract_colors.clicked.connect(self.extract_and_display_colors)
        self.btn_extract_colors.setStyleSheet("""
            background-color: #2ecc71; color: white; font-weight: bold; 
            padding: 8px 15px; border-radius: 4px;
        """)
        toolbar_layout.addWidget(self.btn_extract_colors)

        self.color_palette = QFrame()
        self.color_palette.setFrameShape(QFrame.Shape.StyledPanel)
        self.color_palette.setFixedHeight(50)

        self.color_palette_layout = QHBoxLayout(self.color_palette)
        self.color_palette_layout.setContentsMargins(10, 0, 10, 0)
        self.color_palette_layout.setSpacing(5)
        self.color_palette_layout.addStretch()

        toolbar_layout.addWidget(self.color_palette, 1)

        layout.addWidget(toolbar_widget)

    #HTML 출력 함수
    def update_html_source(self):
        self.left_editor.blockSignals(True)

        raw_html = self.left_editor.toHtml()
        clean_bg_html = re.sub(r'background-color:[^;]+;?', '', raw_html)
        clean_bg_html = re.sub(r'background:[^;]+;?', '', clean_bg_html)
        self.left_editor.setHtml(clean_bg_html)
        self.left_editor.blockSignals(False)

        soup = BeautifulSoup(raw_html, 'html.parser')
        body = soup.find('body')
        if body:
            clean_html=""
            for content in body.contents:
                clean_html += str(content)
        self.right_editor.setPlainText(clean_html.strip())

    #색상 추출
    def extract_and_display_colors(self):
        #레이아웃 초기화
        while self.color_palette_layout.count():
            item = self.color_palette_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.color_palette_layout.addStretch()

        # 2. 색상 추출
        html_data = self.left_editor.toHtml()
        soup = BeautifulSoup(html_data, 'html.parser')
    
        color_table = set()
        
        for tag in soup.find_all(style=True):
            style = tag['style']
            found = re.findall(r'color:\s*(#[0-9a-fA-F]{6}|rgb\(\d+,\s*\d+,\s*\d+\))', style)
            if found:
                color_table.update(found)
        
        self.current_colors = list(color_table)
        
        # 3. 팔레트 버튼 생성
        if not self.current_colors:
            no_color_label = QLabel("추출된 색상이 없습니다.")
            self.color_palette_layout.insertWidget(0, no_color_label)
            return

        for color_code in self.current_colors:
            color_btn = QPushButton()
            color_btn.setFixedSize(30, 30)
            color_btn.setStyleSheet(f"background-color: {color_code}; border: 1px solid #999; border-radius: 15px;")
            color_btn.clicked.connect(lambda checked, c=color_code: self.change_global_color(c))
            
            # 팔레트 레이아웃의 맨 앞에 추가
            self.color_palette_layout.insertWidget(self.color_palette_layout.count()-1, color_btn)

    def change_global_color(self, old_color):
        dialog = ColorPaletteDialog(self)
        
        if dialog.exec():
            new_color_hex = dialog.selected_color 
            
            #색상 변경 로직
            if new_color_hex:
                current_html = self.left_editor.toHtml()
                escaped_old_color = re.escape(old_color)
                clean_html = re.sub(
                    fr'color:\s*{escaped_old_color}', 
                    f'color: {new_color_hex}', 
                    current_html, 
                    flags=re.IGNORECASE
                )

                self.left_editor.setHtml(clean_html)
                
                self.update_html_source()
                self.extract_and_display_colors()

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    ex = TextEditor()
    ex.show()
    sys.exit(app.exec())