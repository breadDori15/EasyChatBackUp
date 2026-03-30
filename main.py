import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    #프로그램 UI 설정 함수
    def initUI(self):
        self.setWindowTitle('편집기 프로토타입')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.label = QLabel("채팅 내역 복붙")
        layout.addWidget(self.label)

        self.editor = QTextEdit()
        self.editor.setAcceptRichText(True)
        layout.addWidget(self.editor)

        button_layout=QHBoxLayout()
        
        self.btn_get_html = QPushButton("HTML 소스 보기")
        self.btn_get_html.clicked.connect(self.show_html_source)
        button_layout.addWidget(self.btn_get_html)

        self.btn_clear = QPushButton("지우기")
        self.btn_clear.clicked.connect(self.editor.clear)
        button_layout.addWidget(self.btn_clear)

        layout.addLayout(button_layout)

    #HTML 출력 함수
    def show_html_source(self):
        html_content = self.editor.toHtml()
        print("---현재 문서의 HTML 구조---")
        print(html_content[:500] + "...")
        self.label.setText("터미널창에서 HTML 소스를 확인하세요")

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    ex = TextEditor()
    ex.show()
    sys.exit(app.exec())