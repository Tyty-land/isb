import warnings

from cryptography.utils import CryptographyDeprecationWarning
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, modes
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
    from cryptography.hazmat.primitives.ciphers.algorithms import TripleDES
from cryptography.hazmat.primitives import hashes
from pydantic import BaseModel, PrivateAttr

from nfc import name_file_crt


class DecrytorText(BaseModel):
    __args_f: list = PrivateAttr(default=None)

    def __init__(self, /, args_f=None, **data: list):
        super().__init__(**data)
        self.__args_f = args_f

    def decryption(self):
        try:
            with open(self.__args_f[1], 'rb') as close_in:
                private_bytes = close_in.read()
            close_key = load_pem_private_key(private_bytes, password=None)
            with open(self.__args_f[2], 'rb') as sym_in:
                c_sym_key = sym_in.read()
            sym_key = close_key.decrypt(c_sym_key,
                                        asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                                                          algorithm=hashes.SHA256(), label=None))
            with open("iv.txt", "rb") as iv_f:
                iv = iv_f.read()
            cipher = Cipher(TripleDES(sym_key), modes.CBC(iv))
            name_file = name_file_crt(self.__args_f[3], "dc_text.txt")

            with open(self.__args_f[0], "rb") as t_file:
                text = t_file.read()

            de_cryptor = cipher.decryptor()
            dc_text = de_cryptor.update(text) + de_cryptor.finalize()

            un_pad = sym_padding.ANSIX923(32).unpadder()
            dc_text = un_pad.update(dc_text) + un_pad.finalize()
            with open(name_file, "w") as ct_file:
                ct_file.write(dc_text.decode('utf-8', errors='ignore'))
        except Exception as ex:
            raise Exception(f" [!] - Какая-то фигня, проверь : {ex}")
