# Fui Obfuscator

from base64 import b85encode
from gzip import compress
from random import choices
from pathlib import Path
import zlib
import base64
import marshal

# Encoding
zlb = lambda in_ : zlib.compress(in_)
b64 = lambda in_ : base64.b64encode(in_)
mar = lambda in_ : marshal.dumps(compile(in_,'<x>','exec'))
note = "# Obfuscated with Fui Obfuscator!\n"

def hexadecimal(code: str = None) -> str:
    code = "".join([f"\\x{car:0>2x}" for car in code.encode()])
    code = f"_=exec;_('{code}')"
    return code

def base85(code: str = None) -> str:
    code = b85encode(code.encode())
    code = (
        code
    ) = ("from base64 import b85decode as _;___=bytes.decode;"f"__=exec;__(___(_({code})))")
    return code

def xor_code(code: str = None, password: str = None) -> str:
    password = password
    if password:
        ask_password = True
        password = password.encode()
        password_lenght = len(password)
    else:
        ask_password = False
        password = choices(list(range(256)), k=40)
        password_lenght = 40
    code = [
        char ^ password[i % password_lenght]
        for i, char in enumerate(code.encode())
    ]
    if ask_password:
        code = (
            "_=input('Password: ').encode();__=len(_);___=exec;_____='';"
            f"\nfor _______,______ in enumerate({code}):_____+=chr"
            "(______^_[_______%__])\n___(_____)"
        )
    else:
        code = (
            f"_={password};__=len(_);___=exec;_____='';\nfor _______,_____"
            f"_ in enumerate({code}):_____+=chr(______^_[_______%__])"
            "\n___(_____)"
        )
    return code

def gzip(code: str = None) -> str:
    code = compress(code.encode())
    code = (
        code
    ) = f"from gzip import decompress as __;_=exec;_(__({code}))"
    return code

def SEncode(data):
    for x in range(5):
        method = repr(b64(zlb(mar(data.encode('utf8'))))[::-1])
        data = "exec(__import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b64decode(%s[::-1]))))" % method
    z = []
    for i in data:
        z.append(ord(i))
    sata = "_ = %s\nexec(''.join(chr(__) for __ in _))" % z
    return note + "exec(str(chr(35)%s));" % '+chr(1)'*10000+sata

def obfuscate_code(code: str) -> str:
    return hexadecimal(base85(xor_code(gzip(code))))

def obfuscate_folder(folder_path: str,prefix:str="",suffix:str=""):
    folder = Path(folder_path)
    for file in list(folder.rglob("*.py")):
        file_path = Path(file)
        file_path_out = file_path.parent.joinpath(prefix+file_path.stem+suffix+".py")
        with open(file_path.as_posix(), "r", encoding="utf-8") as f:
            code = f.read()
        obfuscated = SEncode(code)
        obfuscated = obfuscate_code(obfuscated)
        with open(file_path_out.as_posix(), "w", encoding="utf-8") as f:
            f.write(obfuscated)
