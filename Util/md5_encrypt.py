# 此文件专门处理md5加密

import hashlib


def md5_encrypt(text):
    m5 = hashlib.md5()
    # TypeError: Unicode-objects must be encoded before hashing for python3
    # 每update一次 值就变了
    m5.update(text.encode("utf-8"))
    value = m5.hexdigest()
    return value

if __name__ == "__main__":
    print(md5_encrypt("ccc"))
