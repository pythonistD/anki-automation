import re
import markdown

from model.ankiEntities import AnkiCard



class FileParser:

    def __init__(self, lines:list[str], pattern:str) -> None:
        self.lines = lines
        self.pattern  = pattern

    def parse(self) -> list[AnkiCard]:
        pass

    def md2html(self, line) -> str:
        return markdown.markdown(line)


class MDFileParser(FileParser):

    def __init__(self, lines:list[str], pattern:str) -> None:
        super().__init__(lines, pattern)

    def parse(self)  -> list[AnkiCard]:
        cards = []
        l = 0
        for r in range(1, len(self.lines)):
            if re.search(self.pattern, self.lines[r]) is not None or r == len(self.lines)-1:
                 title  = self.lines[l].replace('\n','').strip()
                 body = ''.join(self.lines[l+1:r])
                 card = AnkiCard(title=self.md2html(title), body=self.md2html(body), tags=list())
                 cards.append(card)
                 l  = r
        return cards


