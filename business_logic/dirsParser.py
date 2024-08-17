import os

class DirsParser:
    ignore_md_files = {"README.md"}
    ignore_dirs = {".git", "static"}

    def __init__(self, path2FileOrDir: str) -> None:
        self.path2FileOrDir = path2FileOrDir

    def conver_all_names_to_abspath(self, base_dir, names:list[str]) -> list[str]:
        res = []
        for n in names:
            s = os.path.join(base_dir, n)
            res.append(s)
        return res


    def get_md_files(self, dirs:list[str]) -> list[str]:
        res = []
        for d in dirs:
            if os.path.isfile(d) and os.path.basename(d) not in self.ignore_md_files and os.path.basename(d).split(".")[1] == "md":
                res.append(d)
        return res


    def get_all_md_files(self, base_dir_path:str) -> list[str]:
        dirs:list[str] = self.conver_all_names_to_abspath(base_dir_path, os.listdir(base_dir_path))
        md_files:list[str] = []
        for d in dirs:
            if (os.path.isdir(d)) and (os.path.basename(d) not in self.ignore_dirs):
                md_files.extend(self.get_all_md_files(d))
        md_files.extend(self.get_md_files(dirs))
        return md_files
    
    def parse_dirs(self) -> list[str]:
        if os.path.isfile(self.path2FileOrDir):
            return [self.path2FileOrDir]
        return self.get_all_md_files(self.path2FileOrDir)