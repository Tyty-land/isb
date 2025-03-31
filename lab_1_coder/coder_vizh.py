def transformer(str_trans: str) -> str:
    """
    This function is needed to convert strings to a specific shape.
    Namely, all characters are uppercase and the string itself is without punctuation marks
    (the list of characters can be updated).
    In the future, the strings returned by this function will be used in message encryption/decryption.
    :param str_trans: the original line
    :return: str_trans - converted string
    """
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
    """
    The heart of the program. Here, the Vision encryption is performed directly or the reverse action, depending
    on the parameter (oper_mod).

    The function is divided into three parts:
    1) Convert text and keyword into an encryption/decryption-friendly format
    2) Creating a string from a repeating key as long as the text
    3) Encryption/Decryption using an offset in the ASCII table

    :param original_text: The initial text for encryption or decryption
    :param key_word: a keyword or sentence (no more than the text itself)
    :param oper_mod: mode switch
    :return: coded_text - Encrypted/Decrypted Text
    """
    alphabet = [chr(1040 + x) for x in range(0, 32)]
    alphabet.append(" ")

    original_text = transformer(original_text)
    key_word = transformer(key_word)

    if len(key_word) > int(len(original_text) / 2):
        key_word = key_word[:int(len(original_text) / 2)]

    writer_files(key_word, "key_word.txt")

    key_string = ""
    for i in range(0, int(len(original_text) / len(key_word) + 1)):
        key_string += key_word
    if len(key_string) > len(original_text):
        key_string = key_string[:-(len(key_string) - len(original_text))]

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
    """
    The purpose of this function is to save a string to a file in an easy-to-read format.
    For example, an encrypted text
    :param text_for_write: the text to save
    :param name_file: the name of the text file
    :return: None
    """
    if ".txt" not in name_file:
        name_file = name_file + ".txt"

    for i in range(0, len(text_for_write)):
        if i % 100 == 0 and i != 0:
            text_for_write = text_for_write[:i] + text_for_write[i] + "\n" + text_for_write[i + 1:]

    with open(name_file, "w", encoding='utf-8') as file:
        file.write(text_for_write)
        print(f"Файл {name_file} создан")


def main() -> None:
    """
    This function simply implements a simple interface for running other functions that are already directly related
    to message encoding. After encrypting the text received from the specified file using a key that the user invents
    himself, the already encrypted text is also saved as a file. The key is saved separately
    :return: None
    """
    oper_mod = int(input("Выберите режим работы(1 - шифруем, 0 - дешифруем)> "))
    text_file = input("Введите путь/название файла с текстом: ")
    if ".txt" not in text_file:
        text_file += ".txt"
    key_word = input("Введите ключ: ")

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
