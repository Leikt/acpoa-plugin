import glob
import os
import re


def build(args):
    def update_datalist():
        files = str(glob.glob("**/*", recursive=True))
        with open('setup.py', 'r') as file:
            text = file.read()
        text = re.sub(r"(files = ).*", rf"\1{files}", text)
        with open('setup.py', 'w') as file:
            file.write(text)

    original_path = os.getcwd()
    os.chdir(args.path)
    if args.data_detection: update_datalist()
    os.system("python3 -m build")
    os.chdir(original_path)
