from dto.dto import UserInputData

from model.ankiEntities import AnkiCard

from business_logic.fileReader import FileReader
from business_logic.fileWriter import CSVWriter
from business_logic.fileParser import MDFileParser

from dotenv import dotenv_values

class BaseView:

    def __init__(self):
        pass

    def get_data(self) -> UserInputData:
        pass

    def get_pattern(self)  -> str:
        pass


    def run_app(self):
        userData: UserInputData = self.get_data()
        reader = FileReader(userData.in_file_path)
        lines: list[str] = reader.read_file()
        pattern= self.get_pattern()
        parser = MDFileParser(lines=lines, pattern=pattern)
        cards:list[AnkiCard]= parser.parse()
        writer  = CSVWriter(userData.out_file_path, cards=cards)
        writer.write()


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

        return UserInputData(in_f, out_f)
    
    def read_from_file(self)  -> list[str]:
        values = dotenv_values(".env")
        file_path = values.get("PFILE")
        if file_path is None:
            file_path = input("Введите путь к файлу: ")

        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readlines()[0].split(" ")

    def read_from_stdin(self) -> list[str]:
        return input("Введите: <path_to_md_file> <path_to_out_file>: ").split(" ")
    
    def get_pattern(self)   -> str:
        val = input("Карточка начинается с:\n (1) # <digit>.\n (2) ## \n (3) Ввести свой патерн\n ")
        pattern = ''
        match val:
            case "1": pattern = r'^#{1}\s'
            case "2": pattern = r'^#{2}\s'
            case "3":
                pattern = input("Введите свой патерн: ")
        return pattern

