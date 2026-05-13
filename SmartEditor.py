import re
from bs4 import BeautifulSoup
from PyQt6.QtWidgets import QTextEdit

class SmartTextEditor(QTextEdit):
    def insertFromMimeData(self, source):
        if source.hasHtml():
            raw_html = source.html()
            soup = BeautifulSoup(raw_html, "html.parser")

            for tag in soup.find_all(True):
                style = tag.get("style", "")
                
                color_match = re.search(r"color:\s*(#[0-9a-fA-F]+|rgb\([^)]+\))", style)
                
                if color_match:
                    tag.attrs = {"style": color_match.group(0)}
                else:
                    if tag.name not in ['p', 'br', 'body', 'html']:
                        tag.unwrap()

            #한국어 인코딩 문제로 decode 사용 중!
            self.insertHtml(soup.decode(formatter=None))
        else:
            super().insertFromMimeData(source)