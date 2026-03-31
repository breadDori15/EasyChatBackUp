import sys
import re
from PyQt6.QtWidgets import (QApplication, QMainWindow, QSplitter, QTextEdit, 
                             QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel, QFrame)
from bs4 import BeautifulSoup

from ColorPalette import ColorPaletteDialog
from SmartEditor import SmartTextEditor

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    #프로그램 UI 설정
    def initUI(self):
        self.setWindowTitle('편집기 프로토타입')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.mode_layout = QHBoxLayout()
        self.btn_toggle_view = QPushButton("HTML")
        self.btn_toggle_view.setFixedWidth(150)
        self.btn_toggle_view.clicked.connect(self.toggle_editor_mode)
        self.mode_layout.addWidget(self.btn_toggle_view)
        self.mode_layout.addStretch()
        layout.addLayout(self.mode_layout)
        
        #body
        self.editor = SmartTextEditor()
        self.editor.setAcceptRichText(True)
        self.editor.setPlaceholderText("여기에 내용을 입력")

        layout.addWidget(self.editor)

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

        #현재 모드(False: 일반, True: HTML)
        self.is_html_mode = False

    def toggle_editor_mode(self):
        if not self.is_html_mode:
            raw_html = self.editor.toHtml()

            soup = BeautifulSoup(raw_html, 'html.parser')
            body = soup.find('body')

            if body:
                clean_content = "".join(str(c) for c in body.contents)
            else:
                clean_content = raw_html

            self.editor.setAcceptRichText(False)
            self.editor.setPlainText(clean_content.strip())

            self.btn_toggle_view.setText("일반 모드")
            self.is_html_mode = True
            self.editor.setStyleSheet("background-color: #2b2b2b; color: #a9b7c6;")

        else:
            current_source = self.editor.toPlainText()

            self.editor.setAcceptRichText(True)
            self.editor.setHtml(current_source)

            self.btn_toggle_view.setText("HTML")
            self.editor.setStyleSheet("background-color: #ffffff;")
            self.is_html_mode = False

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
        html_data = self.editor.toHtml()
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
            if not new_color_hex:
                return
            
            if self.is_html_mode:
                current_text = self.editor.toPlainText()
            else:
                current_text = self.editor.toHtml()

            escaped_old_color = re.escape(old_color)
            updated_text = re.sub(fr'color:\s*{escaped_old_color}', 
                f'color: {new_color_hex}', 
                current_text, 
                flags=re.IGNORECASE
            )
            
            if self.is_html_mode:
                cursor = self.editor.textCursor()
                pos = cursor.position()

                self.editor.setPlainText(updated_text)
                cursor.setPosition(pos)
                self.editor.setTextCursor(cursor)
            else:
                self.editor.setHtml(updated_text)
            
            self.extract_and_display_colors()

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    ex = TextEditor()
    ex.show()
    sys.exit(app.exec())