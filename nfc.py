def name_file_crt(path: str, name_file: str) -> str:
    """
    This function connects the file path and the file name with the extension so that there are no problems.
    :param path: The path to the directory where the file will be stored
    :param name_file: File Name
    :return path_res: The resulting correct file path is
    """
    if ".txt" in path or ".pem" in path:
        return path
    path_res = path + name_file
    if path[len(path) - 1] != '\\' and path != '~':
        path_res = path + "\\" + name_file
    elif path == "~":
        path_res = name_file
    return path_res
