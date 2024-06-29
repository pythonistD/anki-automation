import re
from typing import List
import pprint
import markdown
import csv

def cleanUp(lines: list):
    return [l for l in lines if l != '\n']

def createCards(lines: List[str]):
    cards = [lines[0]]
    l = 1
    for r in range(1, len(lines)):
        
        if re.search(r'#\s*\d', lines[r]) is not None:
            cards.append(lines[l: r])
            l = r
    cards.append(lines[l:])
    return cards

def createCsvFileToImport(cards: List[str]):
    with open('./resources/exam_cards.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, strict=True)

        for card in cards:
            header = markdown.markdown(card[0])
            body = markdown.markdown(''.join(card[1:]))
            writer.writerow([header, body])






def main():
    with open('./resources/Jdk_Jre_Jvm.md', 'r', encoding='utf-8') as f:
        exam = f.readlines()
    noNexam= cleanUp(exam)
    cards = createCards(noNexam)
    createCsvFileToImport(cards)

if __name__ == '__main__':
    main()