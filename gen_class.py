import os

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import serialization, hashes
from pydantic import BaseModel, PrivateAttr

from nfc import name_file_crt
from file_manager import FileManager

class GeneratorKeys(BaseModel):
    __args_f: list = PrivateAttr(default=None)

    def __init__(self, /, args_f=None, **data: list):
        super().__init__(**data)
        self.__args_f = args_f

    def generation(self):
        f_man = FileManager()
        sym_key = os.urandom(int(self.__args_f[3]))
        path_sym = name_file_crt(self.__args_f[0], "symmetric_key.txt")

        keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        close_key = keys
        open_key = keys.public_key()
        path_op = name_file_crt(self.__args_f[1], "open_key.pem")
        path_cl = name_file_crt(self.__args_f[2], "close_key.pem")

        c_sym_key = open_key.encrypt(sym_key,
                                     asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                                                       algorithm=hashes.SHA256(),
                                                       label=None))
        f_man.write(c_sym_key, path_sym, "wb")

        f_man.write(open_key.public_bytes(encoding=serialization.Encoding.PEM,
                                          format=serialization.PublicFormat.SubjectPublicKeyInfo), path_op)
        f_man.write(close_key.private_bytes(encoding=serialization.Encoding.PEM,
                                            format=serialization.PrivateFormat.TraditionalOpenSSL,
                                            encryption_algorithm=serialization.NoEncryption()), path_cl)
