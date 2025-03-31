from typing import List
from time import sleep

def sort_frequencies(array: List[list]) -> List[list]:
    x = 0
    while x != len(array[1]) - 1:
        if array[1][x] < array[1][x + 1]:
            y = x + 1
            while y != 0 and array[1][y - 1] < array[1][y]:
                tmp_frq = array[1][y]
                tmp_ltr = array[0][y]
                array[1][y] = array[1][y - 1]
                array[0][y] = array[0][y - 1]
                array[1][y - 1] = tmp_frq
                array[0][y - 1] = tmp_ltr
                y -= 1
                if y == 0 or array[1][y - 1] >= array[1][y + 1]:
                    x = y
        else:
            x += 1
    return array

def create_frequen_alpha(text: str) -> List[list]:
    alpha_freque = [[], []]
    cnt_all_letter = 0
    for i in range(0, len(text)):
        cnt_all_letter += 1
        if text[i] not in alpha_freque[0]:
            alpha_freque[0].append(text[i])
            alpha_freque[1].append(1)
        else:
            alpha_freque[1][alpha_freque[0].index(text[i])] += 1
    alpha_freque[1] = [cnt_letter / cnt_all_letter for cnt_letter in alpha_freque[1]]
    return sort_frequencies(alpha_freque)

def replace_list(list_els: list, cur: str, new: str) -> list:
    for i in range(len(list_els)):
        if list_els[i] == cur:
            list_els[i] = new
    return list_els

def alpha_replace(data: list, new_alpha: list) -> list:
    text_list = list(data[0])
    for i in range(len(text_list)):
        text_list[i] = "\n"+text_list[i]+"\n"
    for i in range(len(data[1][0])):
        text_list = replace_list(text_list, "\n"+data[1][0][i]+"\n", "\t"+new_alpha[i]+"\t")
        data[1][0][i] = new_alpha[i]
    data[0] = "".join(text_list).replace("\t", "")

    return data

def custom_replace(data: list, cur: str, new: str) -> list:
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
    for i in range(len(text)):
        if i % 100 == 0 and i != 0:
            text = text[:i] + text[i]+"\n" + text[i+1:]
    return text

def print_al_fr(alpha_freque: List[list], cnt_in_line: int) -> None:
    for_print = ['\"' + alpha_freque[0][x] + '\" = ' + str(alpha_freque[1][x]) for x in range(len(alpha_freque[0]))]
    for i in range(len(for_print)):
        if (i+1) % cnt_in_line == 0 and i != 0:
            for_print[i] = for_print[i] + "\n"
    print(" ".join(for_print).replace("\n ", "\n"))

def main() -> None:
    coded_text_file = input("Введите имя/путь файла с зашифрованным сообщением: ")
    if ".txt" not in coded_text_file:
        coded_text_file += ".txt"
    coded_text = ""
    with open(coded_text_file, "r", encoding='utf-8') as file:
        coded_text = file.read()
        if "\n" in coded_text:
            coded_text = coded_text.replace("\n", "")

    alpha_freque_orig = [' ', 'О', 'И', 'Е', 'А', 'Н', 'Т', 'С', 'Р', 'В', 'М', 'Л'
        , 'Д', 'Я', 'К', 'П', 'З', 'Ы', 'Ь', 'У', 'Ч', 'Ж', 'Г'
        , 'Х', 'Ф', 'Й', 'Ю', 'Б', 'Ц', 'Ш', 'Щ', 'Э', 'Ъ']
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
            key_alpha = []
            with open(key_file, "r", encoding='utf-8') as file:
                key_alpha = list(file.read())
            data_list = alpha_replace(data_list, key_alpha)
            print(data_list[1][0])


if __name__ == '__main__':
    main()


