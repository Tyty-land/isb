import argparse

from gen_class import GeneratorKeys
from enc_class import CryptorText
from dec_class import DecrytorText
from file_manager import FileManager


def main() -> None:
    """
    The function is a menu that demonstrates the operation of other functions.
    :return None:
    """
    try:
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-gen', '--generation', nargs=4, metavar=('path_sym', 'path_op', 'path_cl', 'byte'),
                           help='Запускает режим генерации ключей')
        group.add_argument('-enc', '--encryption', nargs=4,
                           metavar=('path_text', 'path_cl', 'path_sym', 'path_en_text'),
                           help='Запускает режим шифрования')
        group.add_argument('-enc_j', '--encryption_json', help='Запускает режим шифрования(пути из file.json)')
        group.add_argument('-dec', '--decryption', nargs=4,
                           metavar=('path_en_text', 'path_cl', 'path_sym', 'path_text'),
                           help='Запускает режим дешифрования')
        group.add_argument('-dec_j', '--decryption_json', help='Запускает режим дешифрования(пути из file.json)')

        args = parser.parse_args()
        f_man = FileManager()

        if args.generation is not None:
            if int(args.generation[3]) < 16:
                args.generation[3] = '16'
            elif int(args.generation[3]) > 24:
                args.generation[3] = '24'
            gen = GeneratorKeys(args.generation)
            gen.generation()
            print("Генерация ключей успешно выполнена(все ключи сохранены по своим путям)")
        elif args.encryption is not None:
            encry = CryptorText(args.encryption)
            encry.encryption()
            print("Шифрование текста выполнено успешно(сохранён по заданному пути)")
        elif args.decryption is not None:
            decry = DecrytorText(args.decryption)
            decry.decryption()
            print("Дешифрование текста выполнено успешно(сохранён по заданному пути)")
        elif args.encryption_json is not None:
            data_js = f_man.read(args.encryption_json)
            encry = CryptorText([data_js['initial_file'],
                                 data_js['secret_key'],
                                 data_js['symmetric_key'],
                                 data_js['encryption_path']])
            encry.encryption()
            print("Шифрование текста выполнено успешно(сохранён по заданному в .json пути)")
        elif args.decryption_json is not None:
            data_js = f_man.read(args.decryption_json)
            decry = DecrytorText([data_js['encryption_file'],
                                  data_js['secret_key'],
                                  data_js['symmetric_key'],
                                  data_js['decryption_path']])
            decry.decryption()
            print("Дешифрование текста выполнено успешно(сохранён по заданному в .json пути)")
    except Exception as ex:
        print(f"WARNING!!:{ex}")


if __name__ == '__main__':
    main()
