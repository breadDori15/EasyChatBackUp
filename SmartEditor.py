import re
from PyQt6.QtWidgets import (QTextEdit)

class SmartTextEditor(QTextEdit):
    def insertFromMimeData(self, source):
        if source.hasHtml():
            raw_html = source.html()
            clean_html = re.sub(r'background-color:[^;]+;?', '', raw_html)
            clean_html = re.sub(r'background:[^;]+;?', '', clean_html)
            clean_html = re.sub(r'font-style:italic;', '', clean_html)
            clean_html = re.sub(r'스냅샷', '', clean_html)

            self.insertHtml(clean_html)
        else:
            super().insertFromMimeData(source)