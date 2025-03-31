def transformer(str_trans: str) -> str:
    not_for_coder = [",", "-", ":", ";", ".", "!", "?", "–", "«", "»"]  # Можно дополнять
    for i in not_for_coder:
        if i in str_trans:
            str_trans = str_trans.replace(i, "")
    for j in range(0, len(str_trans)):
        if ord(str_trans[j]) > 1071:
            str_trans = str_trans[:j] + chr(ord(str_trans[j]) - 32) + str_trans[j + 1:]
        if ord('A') <= ord(str_trans[j]) <= ord('Z'):
            str_trans = str_trans[:j] + chr(ord(str_trans[j]) - ord('A') + 1040) + str_trans[j + 1:]
        if ord('a') <= ord(str_trans[j]) <= ord('z'):
            str_trans = str_trans[:j] + chr(ord(str_trans[j]) - 32 - ord('A') + 1040) + str_trans[j + 1:]

    return str_trans


def coder_vizhener(original_text: str, key_word: str, oper_mod: bool) -> str:
    alphabet = [chr(1040 + x) for x in range(0, 32)]
    alphabet.append(" ")

    # Делаем ключ и исходный текст с заглавными буквами и без знаков препинания
    original_text = transformer(original_text)
    key_word = transformer(key_word)

    if len(key_word) > int(len(original_text) / 2):
        key_word = key_word[:int(len(original_text) / 2)]

    writer_files(key_word, "key_word.txt")

    # Создаём строку из ключевых слов для дальнейшего шифрования текста
    key_string = ""
    for i in range(0, int(len(original_text) / len(key_word) + 1)):
        key_string += key_word
    if len(key_string) > len(original_text):
        key_string = key_string[:-(len(key_string) - len(original_text))]

    # Шифруем/Дешифруем сообщение по Виженеру
    coded_text = original_text
    if oper_mod:
        for i in range(0, len(key_string)):
            final_index = alphabet.index(coded_text[i]) + alphabet.index(key_string[i]) + 1
            if final_index > len(alphabet) - 1:
                final_index = final_index - len(alphabet)
            coded_text = coded_text[:i] + alphabet[final_index] + coded_text[i + 1:]
    else:
        for i in range(0, len(key_string)):
            final_index = alphabet.index(coded_text[i]) - alphabet.index(key_string[i]) - 1
            if final_index < 0:
                final_index = final_index + len(alphabet)
            coded_text = coded_text[:i] + alphabet[final_index] + coded_text[i + 1:]
    return coded_text


def writer_files(text_for_write: str, name_file: str) -> None:
    if ".txt" not in name_file:
        name_file = name_file + ".txt"

    for i in range(0, len(text_for_write)):
        if i % 100 == 0 and i != 0:
            text_for_write = text_for_write[:i] + text_for_write[i] + "\n" + text_for_write[i + 1:]

    with open(name_file, "w", encoding='utf-8') as file:
        file.write(text_for_write)
        print(f"Файл {name_file} создан")


def main() -> None:
    oper_mod = int(input("Выберите режим работы(1 - шифруем, 0 - дешифруем)> "))
    text_file = input("Введите путь/название файла с текстом: ")
    if ".txt" not in text_file:
        text_file += ".txt"
    key_word = input("Введите ключ: ")

    text_string = ""
    with open(text_file, "r", encoding='utf-8') as file:
        text_string = file.read()
        if '\n' in text_string:
            text_string = text_string.replace("\n", "")

    print(text_string)
    name_res_file = "decoded_text"
    if oper_mod:
        name_res_file = "coded_text"
    writer_files(coder_vizhener(text_string, key_word, oper_mod), name_res_file)


if __name__ == '__main__':
    main()
