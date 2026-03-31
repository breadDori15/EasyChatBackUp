import re
from PyQt6.QtWidgets import (QTextEdit)
from PyQt6.QtGui import (QTextCursor)

class SmartTextEditor(QTextEdit):
    def insertFromMimeData(self, source):
        if source.hasHtml():
            raw_html = source.html()
            clean_bg_html = re.sub(r'background-color:[^;]+;?', '', raw_html)
            clean_bg_html = re.sub(r'background:[^;]+;?', '', clean_bg_html)

            self.insertHtml(clean_bg_html)
        else:
            super().insertFromMimeData(source)