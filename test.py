import os
from dotenv import dotenv_values



def conver_all_names_to_abspath(base_dir, names:list[str]) -> list[str]:
    res = []
    for n in names:
        s = os.path.join(base_dir, n)
        res.append(s)
    return res

ignore_md_files = {"README.md"}

def get_md_files(dirs:list[str]) -> list[str]:
    res = []
    for d in dirs:
        if os.path.isfile(d) and os.path.basename(d) not in ignore_md_files and os.path.basename(d).split(".")[1] == "md":
            res.append(d)
    return res

ignore_dirs = {".git", "static"}

def get_all_md_files(base_dir_path:str) -> list[str]:
    dirs:list[str] = conver_all_names_to_abspath(base_dir_path, os.listdir(base_dir_path))
    md_files:list[str] = []
    for d in dirs:
        if (os.path.isdir(d)) and (os.path.basename(d) not in ignore_dirs):
            md_files.extend(get_all_md_files(d))
    md_files.extend(get_md_files(dirs))
    return md_files

def print_md_file_names_and_count(file_paths:list[str]):
    c = 0
    for p in file_paths:
        c += 1
        print(os.path.basename(p))
    print(c)

    


values = dotenv_values(".env")
file_path = values.get("PFILE")
with open(file_path, 'r', encoding='utf-8') as f:
    path_to_base_dir = f.readlines()[0].split(" ")[0]
os.chdir(path_to_base_dir)

md_files_with_cards: list[str] = get_all_md_files(path_to_base_dir)
print_md_file_names_and_count(md_files_with_cards)

'''
full_paths = conver_all_names_to_abspath(path_to_base_dir, dirs_inside_base_dir)
files = get_md_files(full_paths)
print(files)
dirs = get_dirs(full_paths)
print(dirs)
'''