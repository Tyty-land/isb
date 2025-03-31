from typing import List
from time import sleep


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
                tmp_frq = data[1][y]
                tmp_ltr = data[0][y]
                data[1][y] = data[1][y - 1]
                data[0][y] = data[0][y - 1]
                data[1][y - 1] = tmp_frq
                data[0][y - 1] = tmp_ltr
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
    cnt_all_letter = 0
    for i in range(0, len(text)):
        cnt_all_letter += 1
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


def print_al_fr(data: List[list], cnt_in_line: int) -> None:
    """
    The helper function.
    It is needed to correctly display the current alphabet with the frequencies of each letter in it.
    :param data: A list with an alphabet sorted by frequencies and the frequencies themselves
    :param cnt_in_line: The number of letters displayed in one line
    :return: None
    """
    for_print = ['\"' + data[0][x] + '\" = ' + str(data[1][x]) for x in range(len(data[0]))]
    for i in range(len(for_print)):
        if (i+1) % cnt_in_line == 0 and i != 0:
            for_print[i] = for_print[i] + "\n"
    print(" ".join(for_print).replace("\n ", "\n"))


def main() -> None:
    """
    This function is the usual interface of the program. All the functions above are used here.
    The interface itself is cyclical.
    :return: None
    """
    coded_text_file = input("Введите имя/путь файла с зашифрованным сообщением: ")
    if ".txt" not in coded_text_file:
        coded_text_file += ".txt"
    with open(coded_text_file, "r", encoding='utf-8') as file:
        coded_text = file.read()
        if "\n" in coded_text:
            coded_text = coded_text.replace("\n", "")

    alpha_freque_orig = [' ', 'О', 'И', 'Е', 'А', 'Н', 'Т', 'С', 'Р', 'В', 'М', 'Л',
                         'Д', 'Я', 'К', 'П', 'З', 'Ы', 'Ь', 'У', 'Ч', 'Ж', 'Г',
                         'Х', 'Ф', 'Й', 'Ю', 'Б', 'Ц', 'Ш', 'Щ', 'Э', 'Ъ']
    data_list = [coded_text, create_frequen_alpha(coded_text)]

    switch = ""
    while switch != "0":
        print("Текущий текст: ")
        print("")
        print(change_text(data_list[0]))
        print("")
        print("Текущий алфавит: ")
        print("")
        print_al_fr(data_list[1], 4)
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
            data_list = alpha_replace(data_list, alpha_freque_orig)
        elif switch == 'r':
            cur = input("Что заменяем: ")
            new = input("На что заменяем: ")
            data_list = custom_replace(data_list, cur, new)
        elif switch == 's':
            with open("key_alpha.txt", "w", encoding='utf-8') as file:
                file.write("".join(data_list[1][0]))
            print("Ключ сохранён")
            with open("text_by_key.txt", "w", encoding='utf-8') as file:
                file.write(change_text(data_list[0]))
            print("Текст сохранён")
            sleep(2)
        elif switch == 'k':
            key_file = input("Укажите путь до файла с ключом: ")
            if ".txt" not in key_file:
                key_file = key_file + ".txt"
            with open(key_file, "r", encoding='utf-8') as file:
                key_alpha = list(file.read())
            data_list = alpha_replace(data_list, key_alpha)
            print(data_list[1][0])


if __name__ == '__main__':
    main()
