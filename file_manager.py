import json

class FileManager:
    _path_file: str = ""
    _method: str = ""

    def __init__(self, path_file="", method=""):
        self._path_file = path_file
        self._method = method

    def read(self, path_file="", method=""):
        try:
            self._path_file = path_file if path_file != "" else self._path_file
            self._method = method if method != "" else self._method
            if ".json" not in self._path_file and self._method != "r":
                with open(self._path_file, self._method) as f:
                    return f.read()
            elif ".json" not in self._path_file and self._method == "r":
                with open(self._path_file, self._method, encoding='utf-8') as f:
                    return f.read()
            else:
                with open(self._path_file, "r") as f:
                    return json.load(f)
        except Exception as ex:
            raise Exception(f" [!] - Какая-то фигня, проверь : {ex}")

    def write(self, data, path_file="", method=""):
        try:
            self._path_file = path_file if path_file != "" else self._path_file
            self._method = method if method != "" else self._method
            with open(self._path_file, self._method) as f:
                f.write(data)
        except Exception as ex:
            raise Exception(f" [!] - Какая-то фигня, проверь : {ex}")
