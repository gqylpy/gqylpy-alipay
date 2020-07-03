class ED:
    # Encrypt Decrypt

    _offset = -1
    _split = '-'
    _flag = 65535

    def __init__(self, offset: int = None):
        # offset: 偏移量，加密和解密需一致，
        # 偏移量不可为0或字符长度的整数倍
        self.offset = offset or self._offset

    def encrypt(self, data: str):
        """加密函数"""
        lst = [ord(i) for i in data]
        len(lst) == 1 and lst.append(self._flag)
        for i in range(len(lst)):
            lst[i] += self._(lst, i)
        return self._split.join(str(i) for i in lst)

    def decrypt(self, data: str):
        """解密函数"""
        lst = [int(i) for i in data.split(self._split)]
        for i in range(len(lst) - 1, -1, -1):
            lst[i] -= self._(lst, i)
        lst[-1] == self._flag and lst.pop()
        return ''.join(chr(i) for i in lst)

    def _(self, data, i):
        """索引加偏移量余长度取值"""
        return data[(i + self.offset) % len(data)]


def edf(data: ..., decrypt: bool = False):
    # Encrypt decrypt function.
    ed = ED()

    if isinstance(data, (int, float)):
        data = str(data)

    if decrypt:
        return ed.decrypt(data)

    return ed.encrypt(data)
