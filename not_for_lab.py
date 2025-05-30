import json
import os
import argparse
import warnings

from cryptography.utils import CryptographyDeprecationWarning
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, modes

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
    from cryptography.hazmat.primitives.ciphers.algorithms import TripleDES


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


def generation(args_f: list) -> None:
    """
    The function generates encryption keys: symmetric, public, and private.
    All of them are saved to files in the directory they specify
    (the symmetric key is encrypted with the RSA algorithm using the public key)
    :param args_f: Array of paths obtained from arg.parser()
    :return None:
    """
    try:
        sym_key = os.urandom(int(args_f[3]))
        path_sym = name_file_crt(args_f[0], "symmetric_key.txt")

        keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        close_key = keys
        open_key = keys.public_key()
        path_op = name_file_crt(args_f[1], "open_key.pem")
        path_cl = name_file_crt(args_f[2], "close_key.pem")

        c_sym_key = open_key.encrypt(sym_key,
                                     asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                                                       algorithm=hashes.SHA256(),
                                                       label=None))
        with open(path_sym, "wb") as sym_out:
            sym_out.write(c_sym_key)

        with open(path_op, 'wb') as open_out:
            open_out.write(open_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                 format=serialization.PublicFormat.SubjectPublicKeyInfo))
        with open(path_cl, 'wb') as close_out:
            close_out.write(close_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                    encryption_algorithm=serialization.NoEncryption()))
    except Exception as ex:
        raise Exception(f" [!] - Какая-то фигня, проверь : {ex}")


def encry_decry(args_f: list, oper: bool) -> None:
    """
    The function encrypts and decrypts text files, the mode selection depends on the value of the "oper" parameter
    All encryption and decryption results are written to a file using the specified path.
    :param args_f: Array of paths obtained from arg.parser()
    :param oper: Toggle switch for mode selection
    :return None:
    """
    try:
        with open(args_f[1], 'rb') as close_in:
            private_bytes = close_in.read()
        close_key = load_pem_private_key(private_bytes, password=None)
        with open(args_f[2], 'rb') as sym_in:
            c_sym_key = sym_in.read()
        sym_key = close_key.decrypt(c_sym_key,
                                    asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                                                      algorithm=hashes.SHA256(), label=None))
        if not oper:
            with open("iv.txt", "rb") as iv_f:
                iv = iv_f.read()
        else:
            iv = os.urandom(8)
            with open("iv.txt", "wb") as iv_f:
                iv_f.write(iv)
        cipher = Cipher(TripleDES(sym_key), modes.CBC(iv))
        name_file = name_file_crt(args_f[3], "c_text.txt") if oper else name_file_crt(args_f[3], "dc_text.txt")
        if oper:
            with open(args_f[0], "r", encoding='utf-8') as t_file:
                text = t_file.read()
            pad = sym_padding.ANSIX923(32).padder()
            text = bytes(text, 'utf-8')
            padded_text = pad.update(text) + pad.finalize()

            encryptor = cipher.encryptor()
            c_text = encryptor.update(padded_text) + encryptor.finalize()

            with open(name_file, "wb") as ct_file:
                ct_file.write(c_text)
        else:
            with open(args_f[0], "rb") as t_file:
                text = t_file.read()

            de_cryptor = cipher.decryptor()
            dc_text = de_cryptor.update(text) + de_cryptor.finalize()

            un_pad = sym_padding.ANSIX923(32).unpadder()
            dc_text = un_pad.update(dc_text) + un_pad.finalize()
            with open(name_file, "w") as ct_file:
                ct_file.write(dc_text.decode('utf-8', errors='ignore'))
    except Exception as ex:
        raise Exception(f" [!] - Какая-то фигня, проверь : {ex}")


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
        group.add_argument('-enc', '--encryption', nargs=4, metavar=('path_text', 'path_cl', 'path_sym', 'path_en_text')
                           , help='Запускает режим шифрования')
        group.add_argument('-enc_j', '--encryption_json', help='Запускает режим шифрования(пути из file.json)')
        group.add_argument('-dec', '--decryption', nargs=4, metavar=('path_en_text', 'path_cl', 'path_sym', 'path_text')
                           , help='Запускает режим дешифрования')
        group.add_argument('-dec_j', '--decryption_json', help='Запускает режим дешифрования(пути из file.json)')

        args = parser.parse_args()

        if args.generation is not None:
            if int(args.generation[3]) < 16:
                args.generation[3] = '16'
            elif int(args.generation[3]) > 24:
                args.generation[3] = '24'
            generation(args.generation)
            print("Генерация ключей успешно выполнена(все ключи сохранены по своим путям)")
        elif args.encryption is not None:
            encry_decry(args.encryption, True)
            print("Шифрование текста выполнено успешно(сохранён по заданному пути)")
        elif args.decryption is not None:
            encry_decry(args.decryption, False)
            print("Дешифрование текста выполнено успешно(сохранён по заданному пути)")
        elif args.encryption_json is not None:
            with open(args.encryption_json, "r") as js_file:
                data_js = json.load(js_file)
            encry_decry([data_js['initial_file'],
                         data_js['secret_key'],
                         data_js['symmetric_key'],
                         data_js['encryption_path']], True)
            print("Шифрование текста выполнено успешно(сохранён по заданному в .json пути)")
        elif args.decryption_json is not None:
            with open(args.decryption_json, "r") as js_file:
                data_js = json.load(js_file)
            encry_decry([data_js['encryption_file'],
                         data_js['secret_key'],
                         data_js['symmetric_key'],
                         data_js['decryption_path']], False)
            print("Дешифрование текста выполнено успешно(сохранён по заданному в .json пути)")
    except Exception as ex:
        print(f"WARNING!!:{ex}")


if __name__ == '__main__':
    main()
