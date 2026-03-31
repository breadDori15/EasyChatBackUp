import re
from PyQt6.QtWidgets import QTextEdit, QFrame, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QTextCursor

class EditableBlock(QFrame):
    # 클릭 시 (자기객체, 컨트롤키여부) 전달
    clicked = pyqtSignal(object, bool)
    text_changed = pyqtSignal()

    def __init__(self, html_content="", parent=None):
        super().__init__(parent)
        self.is_selected = False
        self.initUI(html_content)

    def initUI(self, html_content):
        self.setObjectName("Block")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # 각 블록은 내부적으로 QTextEdit을 가짐 (노션의 한 행처럼 동작)
        self.editor = QTextEdit()
        self.editor.setHtml(html_content)
        self.editor.setAcceptRichText(True)
        self.editor.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.editor.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.editor.document().contentsChanged.connect(self.update_height)
        self.editor.document().contentsChanged.connect(self.text_changed.emit)
        
        # 배경색 제거 로직 (이전 챕터 적용)
        self.editor.installEventFilter(self) 
        
        layout.addWidget(self.editor)
        self.update_height()
        self.update_style()

    def update_height(self):
        # 텍스트 양에 따라 높이 자동 조절
        doc_height = self.editor.document().size().height()
        self.editor.setFixedHeight(int(doc_height) + 10)
        self.setFixedHeight(int(doc_height) + 20)

    def update_style(self):
        border = "#3498db" if self.is_selected else "transparent"
        bg = "#f4f4f4" if self.is_selected else "white"
        self.setStyleSheet(f"""
            #Block {{
                border: 2px solid {border};
                background-color: {bg};
                border_radius: 4px;
            }}
        """)

    def mousePressEvent(self, event):
        # 블록 여백 클릭 시 선택 로직
        modifiers = event.modifiers()
        is_ctrl = modifiers == Qt.KeyboardModifier.ControlModifier
        self.clicked.emit(self, is_ctrl)
        super().mousePressEvent(event)

    def set_block_color(self, hex_color):
        # 블록 내부 텍스트 전체 색상 변경
        cursor = self.editor.textCursor()
        cursor.select(QTextCursor.SelectionType.Document)
        
        current_html = self.editor.toHtml()
        # 기존 색상 태그 제거 후 새 색상 적용 (정규식 활용 가능)
        new_html = f"<div style='color: {hex_color};'>{self.editor.toPlainText()}</div>"
        self.editor.setHtml(new_html)