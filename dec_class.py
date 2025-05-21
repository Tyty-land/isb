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

class DecrytorText(BaseModel):
    __args_f: list = PrivateAttr(default=None)

    def __init__(self, /, args_f=None, **data: list):
        super().__init__(**data)
        self.__args_f = args_f

    def decryption(self):
        f_man = FileManager(self.__args_f[1], "rb")
        private_bytes = f_man.read()
        close_key = load_pem_private_key(private_bytes, password=None)
        c_sym_key = f_man.read(self.__args_f[2])
        sym_key = close_key.decrypt(c_sym_key,
                                    asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                                                      algorithm=hashes.SHA256(), label=None))

        iv = f_man.read("iv.txt")

        cipher = Cipher(TripleDES(sym_key), modes.CBC(iv))
        path_file = name_file_crt(self.__args_f[3], "dc_text.txt")
        text = f_man.read(self.__args_f[0])

        de_cryptor = cipher.decryptor()
        dc_text = de_cryptor.update(text) + de_cryptor.finalize()

        un_pad = sym_padding.ANSIX923(32).unpadder()
        dc_text = un_pad.update(dc_text) + un_pad.finalize()
        f_man.write(dc_text.decode('utf-8', errors='ignore'), path_file, "w")
