import json
import os
from PyQt6.QtWidgets import QColorDialog, QDialog, QGridLayout, QHBoxLayout, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class ColorPaletteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("새 색상 선택")
        self.setWindowFlag(Qt.WindowType.Popup)
        self.selected_color = None
        self.db_path = "user_colors.json"

        self.default_colors = ['#363636']
        self.user_color = self.load_user_colors() # 로드 시 user_color 리스트 초기화

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("<b>색상 선택</b>"))

        btn_add_custom = QPushButton("+ 추가")
        btn_add_custom.setFixedSize(50, 25)
        btn_add_custom.setStyleSheet("font-size: 11px; background-color: #eee; border-radius: 3px;")
        btn_add_custom.clicked.connect(self.add_new_custom_color)
        header_layout.addWidget(btn_add_custom)

        layout.addLayout(header_layout)

        self.grid = QGridLayout()
        self.grid.setSpacing(8)
        self.refresh_grid()

        layout.addLayout(self.grid)

    def refresh_grid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
        all_colors = self.default_colors + self.user_color
        
        for i, color_code in enumerate(all_colors):
            btn = QPushButton()
            btn.setFixedSize(35, 35)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color_code}; 
                    border: 1px solid #ccc; 
                    border-radius: 4px;
                }}
                QPushButton:hover {{ border: 2px solid #3498db; }}
            """)
            # lambda를 사용하여 클릭 시 해당 색상을 선택하도록 연결
            btn.clicked.connect(lambda checked, c=color_code: self.color_selected(c))
            self.grid.addWidget(btn, i // 6, i % 6)

    def add_new_custom_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            new_hex = color.name().upper()
            if new_hex not in self.default_colors and new_hex not in self.user_color:
                self.user_color.append(new_hex)
                self.save_user_colors()
                self.refresh_grid()

    def color_selected(self, color):
        self.selected_color = color
        self.accept()

    def load_user_colors(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else []
            except:
                return []
        return []
    
    def save_user_colors(self):
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.user_color, f)