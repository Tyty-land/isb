import os
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
from file_manager import FileManager

class CryptorText(BaseModel):
    __args_f: list = PrivateAttr(default=None)

    def __init__(self, /, args_f=None, **data: list):
        super().__init__(**data)
        self.__args_f = args_f

    def encryption(self):
        f_man = FileManager(self.__args_f[1], "rb")
        private_bytes = f_man.read()
        close_key = load_pem_private_key(private_bytes, password=None)
        c_sym_key = f_man.read(self.__args_f[2])
        sym_key = close_key.decrypt(c_sym_key,
                                    asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                                                      algorithm=hashes.SHA256(), label=None))

        iv = os.urandom(8)
        f_man.write(iv, "iv.txt", "wb")

        cipher = Cipher(TripleDES(sym_key), modes.CBC(iv))
        name_file = name_file_crt(self.__args_f[3], "c_text.txt")
        text = f_man.read(self.__args_f[0], "r")
        pad = sym_padding.ANSIX923(32).padder()
        text = bytes(text, 'utf-8')
        padded_text = pad.update(text) + pad.finalize()

        encryptor = cipher.encryptor()
        c_text = encryptor.update(padded_text) + encryptor.finalize()

        f_man.write(c_text, name_file, "wb")
