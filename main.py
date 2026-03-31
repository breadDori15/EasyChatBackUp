import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplitter, QTextEdit, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    #프로그램 UI 설정 함수
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

    #HTML 출력 함수
    def update_html_source(self):
        html_content = self.left_editor.toHtml()
        self.right_editor.setPlainText(html_content)

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    ex = TextEditor()
    ex.show()
    sys.exit(app.exec())