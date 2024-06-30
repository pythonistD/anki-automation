import csv

from model.ankiEntities import AnkiCard

class FileWriter:

    def __init__(self) -> None:
        pass

    def __init__(self, path: str, cards: list[AnkiCard]):
        self.path = path
        self.cards = cards


    def write(self):
        pass


class CSVWriter(FileWriter):

    def __init__(self, path: str, cards: list[AnkiCard]):
        super().__init__(path, cards)

    def write(self):
        with open(self.path, 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, strict=True)
            #writer.writerow(['front', 'back'])
            for card in self.cards:
                writer.writerow([card.title, card.body])