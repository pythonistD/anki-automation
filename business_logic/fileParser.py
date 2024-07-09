import re
import markdown
import os
import shutil
from PIL import Image

from model.ankiEntities import AnkiCard

ANKI_MEDIA = r"C:\Users\Professional\AppData\Roaming\Anki2\1-й пользователь\collection.media"


class FileParser:

    def __init__(self, lines:list[str], pattern:str, path2File:str) -> None:
        self.lines = lines
        self.pattern  = pattern
        self.path2File = path2File

    def parse(self) -> list[AnkiCard]:
        pass

    def handleMedia(lines: list[str])-> None:
        pass

    def md2html(self, line) -> str:
        return markdown.markdown(line)


class MDFileParser(FileParser):

    def __init__(self, lines:list[str], pattern:str, path2File) -> None:
        super().__init__(lines, pattern, path2File)

    def getPathToMdFileDir(path:str) -> str:
        pass


    def handleMedia(self, lines: list[str]) -> list[str]:
        newBody = []
        for l in lines:
            lineWithMedia = re.search(r'(!\[.*\])(\(.*\))', l)
            if lineWithMedia:
                part1 = lineWithMedia.group(0)
                part2 = lineWithMedia.group(1)
                part3 = lineWithMedia.group(2)
                oldPath = part3.replace('(', "").replace(')', "")

                fileDir = os.path.basename(os.path.dirname(oldPath))
                fileName = os.path.basename(oldPath)
                md_file_dir = os.path.dirname(os.path.abspath(self.path2File))
                absolute2Image = md_file_dir + '\\' + fileDir + '\\' + fileName

                ankiPathToImage:str = self.copyImage(absolute2Image, ANKI_MEDIA)
                newLink = part2 + '(' + fileName + ')'
                print(newLink)
                newBody.append("\n")
                newBody.append(newLink)
                newBody.append("\n")
            else:
                newBody.append(l)
        return newBody



    def copyImage(self, source_path:str, destination_dir:str) -> str:
        try:
            # Проверяем, существует ли исходный файл
            if not os.path.isfile(source_path):
                print(f"Source file '{source_path}' does not exist.")
                return
            # Проверяем, существует ли целевая директория, если нет, создаем ее
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
            
            # Определяем имя файла
            file_name = os.path.basename(source_path)
            
            # Определяем полный путь к целевому файлу
            destination_path = os.path.join(destination_dir, file_name)
            
            # Копируем файл
            image = Image.open(source_path)
            image.save(destination_path)
            
            print(f"File '{source_path}' successfully copied to '{destination_path}'.")
            return destination_path
    
        except Exception as e:
            print(f"An error occurred: {e}")


    def parse(self)  -> list[AnkiCard]:
        cards = []
        l = 0
        for r in range(1, len(self.lines)):
            if re.search(self.pattern, self.lines[r]) is not None or r == len(self.lines)-1:
                 title  = self.lines[l].replace('\n','').strip()
                 newLines = self.handleMedia(self.lines[l+1:r])
                 body = ''.join(newLines)
                 card = AnkiCard(title=self.md2html(title), body=self.md2html(body), tags=list())
                 cards.append(card)
                 l  = r
        return cards


