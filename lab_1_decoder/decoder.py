from typing import List
from time import sleep

from const_fila import ALPHA_FREQUE_ORIG, KEY_ALPHA_NF, TEXT_BY_KEY_NF, ALPHA_BY_FREQUENCIES


def sort_frequencies(data: List[list]) -> List[list]:
    """
    Special bubble sorting for a list of two lists. In fact, only the list of frequencies themselves is sorted,
    but the items in the list with letters change according to the list of frequencies.
    :param data: A list with an alphabet sorted by frequencies and the frequencies themselves
    :return: data - sorted data
    """
    x = 0
    while x != len(data[1]) - 1:
        if data[1][x] < data[1][x + 1]:
            y = x + 1
            while y != 0 and data[1][y - 1] < data[1][y]:
                data[1][y], data[1][y - 1] = data[1][y - 1], data[1][y]
                data[0][y], data[0][y - 1] = data[0][y - 1], data[0][y]
                y -= 1
                if y == 0 or data[1][y - 1] >= data[1][y + 1]:
                    x = y
        else:
            x += 1
    return data


def create_frequen_alpha(text: str) -> List[list]:
    """
    This function allows you to find unique characters in the text, compose an alphabet from them,
    and sort them by their frequency of occurrence in the text itself.
    Accordingly, an array of frequencies of each symbol is formed, also sorted.
    :param text: the text from which the unique characters are found
    :return: sort_frequencies(data) - a list with a list of characters by frequency, as well as a list of frequencies
    """
    data = [[], []]
    cnt_all_letter = len(text)
    for i in range(0, cnt_all_letter):
        if text[i] not in data[0]:
            data[0].append(text[i])
            data[1].append(1)
        else:
            data[1][data[0].index(text[i])] += 1
    data[1] = [cnt_letter / cnt_all_letter for cnt_letter in data[1]]
    return sort_frequencies(data)


def replace_list(list_els: list, cur: str, new: str) -> list:
    """
    The helper function.
    An analog of the .replace() method for lists only
    :param list_els: The list that we are changing
    :param cur: The element that we replace
    :param new: The element to replace it with
    :return: list_els - the modified list
    """
    for i in range(len(list_els)):
        if list_els[i] == cur:
            list_els[i] = new
    return list_els


def alpha_replace(data: list, new_alpha: list) -> list:
    """
    The function changes the alphabet to a new one without touching the frequencies.
    :param data: A list with an alphabet sorted by frequencies and the frequencies themselves
    :param new_alpha: The new alphabet
    :return: data - changed data
    """
    text_list = list(data[0])
    for i in range(len(text_list)):
        text_list[i] = "\n"+text_list[i]+"\n"
    for i in range(len(data[1][0])):
        text_list = replace_list(text_list, "\n"+data[1][0][i]+"\n", "\t"+new_alpha[i]+"\t")
        data[1][0][i] = new_alpha[i]
    data[0] = "".join(text_list).replace("\t", "")

    return data


def custom_replace(data: list, cur: str, new: str) -> list:
    """
    The function is needed to change the characters in the current text and alphabet to new ones.
    Each character from the string of characters that we are changing corresponds to a character from the string
    of characters that we are changing by index
    :param data: A list with an alphabet sorted by frequencies and the frequencies themselves
    :param cur: A string of characters that we are changing
    :param new: The string of characters to change to
    :return: data - changed data
    """
    for i in range(len(cur)):
        if cur[i] in data[0]:
            if new[i] in data[1][0] and new[i] in data[0]:
                for j in range(len(data[0])):
                    if data[0][j] == new[i]:
                        data[0] = data[0][:j] + cur[i] + data[0][j + 1:]
                    elif data[0][j] == cur[i]:
                        data[0] = data[0][:j] + new[i] + data[0][j + 1:]
                sp = 0
                for j in range(len(data[1][0])):
                    if data[1][0][j] == cur[i]:
                        data[1][0][j] = new[i]
                        sp += 1
                    elif data[1][0][j] == new[i]:
                        data[1][0][j] = cur[i]
                        sp += 1
                    if sp == 2:
                        break
            else:
                data[0] = data[0].replace(cur[i], new[i])
                data[1][0][data[1][0].index(cur[i])] = new[i]

    return data


def change_text(text: str) -> str:
    """
    The helper function.
    It is needed for the readable division of a string into substrings, that is, through indentation.
    :param text: current text
    :return: text - converted text
    """
    for i in range(len(text)):
        if i % 100 == 0 and i != 0:
            text = text[:i] + text[i]+"\n" + text[i+1:]
    return text


def print_al_fr(data: List[list], cnt_in_line: int) -> str:
    """
    The helper function.
    It is needed to correctly display the current alphabet with the frequencies of each letter in it.
    :param data: A list with an alphabet sorted by frequencies and the frequencies themselves
    :param cnt_in_line: The number of letters displayed in one line
    :return: None
    """
    for_print = ['\"' + data[0][x] + '\" = ' + str(data[1][x]) for x in range(len(data[0]))]
    for i in range(len(for_print)):
        if (i+1) % cnt_in_line == 0:
            for_print[i] = for_print[i] + "\n"
    return " ".join(for_print).replace("\n ", "\n")

def reader_file(name_file: str) -> str:
    try:
        if ".txt" not in name_file:
            name_file += ".txt"
        with open(name_file, "r", encoding='utf-8') as file:
            text_file = file.read()
        return text_file
    except FileNotFoundError:
        raise FileNotFoundError(f" [!] - Файл {name_file} не найден")

def writer_file(name_file: str, text_for_file: str) -> None:
    try:
        if ".txt" not in name_file:
            name_file += ".txt"
        with open(name_file, "w", encoding='utf-8') as file:
            file.write(text_for_file)
        print(f"Файл с именем {name_file} сохранён")
    except Exception as ex:
        raise Exception(f" [!] - Какая-то фигня, проверь : {ex}")

def main() -> None:
    """
    This function is the usual interface of the program. All the functions above are used here.
    The interface itself is cyclical.
    :return: None
    """
    try:
        coded_text_file = input("Введите имя/путь файла с зашифрованным сообщением: ")
        coded_text = reader_file(coded_text_file).replace("\n", "")

        data_list = [coded_text, create_frequen_alpha(coded_text)]

        switch = ""
        while switch != "0":
            print("Текущий текст: ")
            print("")
            print(change_text(data_list[0]))
            print("")
            print("Текущий алфавит: ")
            print("")
            print(print_al_fr(data_list[1], 4))
            print("_______________Меню_______________")
            print("[f] - Применить частотную замену")
            print("[r] - Заменить")
            print("[s] - Сохранить текущий ключ/текст")
            print("[k] - Использовать ключ")
            print("[0] - Выход")
            print("----------------------------------")
            switch = input("> ")
            print("")
            if switch == 'f':
                data_list = alpha_replace(data_list, ALPHA_FREQUE_ORIG)
            elif switch == 'r':
                cur = input("Что заменяем: ")
                new = input("На что заменяем: ")
                data_list = custom_replace(data_list, cur, new)
            elif switch == 's':
                writer_file(KEY_ALPHA_NF, "".join(data_list[1][0]))
                writer_file(TEXT_BY_KEY_NF, change_text(data_list[0]))
                writer_file(ALPHA_BY_FREQUENCIES, print_al_fr(data_list[1], 1))
                sleep(2)
            elif switch == 'k':
                key_file = input("Укажите путь до файла с ключом: ")
                key_alpha = list(reader_file(key_file))
                data_list = alpha_replace(data_list, key_alpha)
                print(data_list[1][0])
    except Exception as ex:
        print(f"WARNING!!:{ex}")


if __name__ == '__main__':
    main()
