# aiutils.py
import os
import datetime

class AiUtils():
    def __init__(self) -> None:
        pass

    @staticmethod
    def validate_file_path(path, extension, default_name):
        path = path.replace('\\', '/')
        if extension[0] != '.':
            extension =  '.' + extension
        if path[-len(extension):] == extension:
            folder_path = path.rsplit("/", 1)[0]
            os.makedirs(folder_path, exist_ok=True)
        else:
            if path[-1:] != "/":
                path += "/"
            os.makedirs(path, exist_ok=True)
            name = default_name + "_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
            try:
                file_list = os.listdir(path)
            except:
                file_list = []
            i = 0
            while name + extension in file_list:
                i += 1
                name += "({})".format(i)
            name += extension
            path += name
        #print(path)
        return path

    @staticmethod
    def validate_folder_path(path, make_folder: bool):
        path = path.replace('\\', '/')
        if path[-1:] != '/':
            path += '/'
        if make_folder:
            os.makedirs(path, exist_ok=True)
        return path