import os
from dotenv import dotenv_values



def conver_all_names_to_abspath(base_dir, names:list[str]):
    res = []
    for n in names:
        s = conver_dir_name_to_abspath(base_dir, n)
        res.append(s)
    return res

def conver_dir_name_to_abspath(base_dir, name):
    return base_dir + "\\" + name

def get_md_files(dirs:list[str]):
    res = []
    for d in dirs:
        if os.path.isfile(d) and os.path.basename(d).split(".")[1] == "md":
            res.append(d)
    return res

def get_dirs(dirs:list[str]):
    res = []
    for d in dirs:
        if os.path.isdir(d):
            res.append(d)
    return res



values = dotenv_values(".env")
file_path = values.get("PFILE")
with open(file_path, 'r', encoding='utf-8') as f:
    path_to_base_dir = f.readlines()[0].split(" ")[0]
dirs_inside_base_dir = os.listdir(path_to_base_dir)

full_paths = conver_all_names_to_abspath(path_to_base_dir, dirs_inside_base_dir)
files = get_md_files(full_paths)
print(files)
dirs = get_dirs(full_paths)
print(dirs)
