import markdown


class FileReader:

    def __init__(self, dir_path: str) -> None:
        self.file_path = dir_path

    def open_dir(self):
        pass


    def read_file(self)  -> list[str]:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return lines
