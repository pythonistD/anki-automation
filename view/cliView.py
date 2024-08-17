from dto.dto import UserInputData

from model.ankiEntities import AnkiCard, Anki

from business_logic.fileReader import FileReader
from business_logic.fileWriter import CSVWriter
from business_logic.fileParser import MDFileParser
from business_logic.dirsParser import DirsParser

from dotenv import dotenv_values
import os

class BaseView:

    def __init__(self):
        pass

    def get_data(self) -> UserInputData:
        pass

    def get_pattern(self)  -> str:
        pass

    def get_anki_package_name(self) -> str:
        pass

    def change_working_dir(self, path_to_root_dir:str):
        os.chdir(path_to_root_dir)

    def validate_userData(self, in_file_path:str, out_file_path:str):
        if not os.path.isabs(in_file_path) or not os.path.isabs(out_file_path):
            raise Exception("Пути до файлов должны быть абсолютными!")
        if not os.path.isdir(out_file_path):
            raise Exception("Вторым аргументом должно идти имя директории, где будут сохранены карточки!")

    def create_csv_from_md_file(self, abs_path_to_md_file: str, abs_path_to_csv_file: str, pattern:str, anki_instance: Anki):
        reader = FileReader(abs_path_to_md_file)
        lines: list[str] = reader.read_file()
        parser = MDFileParser(lines=lines, pattern=pattern, path2File=abs_path_to_md_file)
        cards:list[AnkiCard]= parser.parse()
        media_images: list[str] = parser.media_images
        '''
        Добавляем карточки в колоду, чтобы не нужно было импортировать csv вручную
        '''
        anki_instance.add_bunch_of_media_image(media_images)
        anki_instance.create_bunch_of_cards(cards)

        writer  = CSVWriter(abs_path_to_csv_file, cards=cards)
        writer.write()

    def get_csv_out_file_path(self, base_csv_path:str, file_basename:str) -> str:
        file_name = file_basename.split(".")[0] + ".csv"
        return os.path.join(base_csv_path, file_name)


    def run_app(self):
        anki_instance: Anki = Anki()
        userData: UserInputData = self.get_data()
        pattern= self.get_pattern()
        anki_package_name:str = self.get_anki_package_name()
        #self.change_working_dir(userData.in_file_path)
        dirsParser: DirsParser = DirsParser(userData.in_file_path)
        all_md_files = dirsParser.parse_dirs()
        for md in all_md_files:
            csv_file_path = self.get_csv_out_file_path(userData.out_file_path, os.path.basename(md))
            self.create_csv_from_md_file(md, csv_file_path, pattern, anki_instance)
        '''
        Создаём колоду Anki
        '''
        path2anki_package = os.path.join(userData.out_file_path, anki_package_name)
        anki_instance.generate_anki_package_of_cards(path2anki_package)


class CLIView(BaseView):
    def __init__(self):
        super().__init__()

    def get_data(self) -> UserInputData:
        mode = input("Выберите режим работы приложения:  (1) Извлечение из файла  (2) Извлечение из stdin:  ")
        match mode:
            case "1": 
                in_f, out_f = self.read_from_file()
            case  "2":
                in_f, out_f  = self.read_from_stdin()

        self.validate_userData(in_f, out_f)

        return UserInputData(in_f, out_f)
    
    def read_from_file(self)  -> list[str]:
        values = dotenv_values(".env")
        file_path = values.get("PFILE")
        if file_path is None:
            file_path = input("Введите путь к файлу: ")

        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readlines()[0].split(" ")

    def read_from_stdin(self) -> list[str]:
        return input("Введите: <path_to_md_file_or_dir> <path_to_out_dir>: ").split(" ")
    
    def get_pattern(self)   -> str:
        val = input("Карточка начинается с:\n (1) # <digit>.\n (2) ## \n (3) Ввести свой патерн\n ")
        pattern = ''
        match val:
            case "1": pattern = r'^#{1}\s'
            case "2": pattern = r'^#{2}\s'
            case "3":
                pattern = input("Введите свой патерн: ")
        return pattern

    def get_anki_package_name(self) -> str:
        package_name:str = input("Введите имя для колоды:\n")
        if package_name.strip() != "":
            return package_name
        raise Exception("Имя не должно быть путь пустым")
