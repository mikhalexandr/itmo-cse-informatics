import datetime


class BinCodec:
    @staticmethod
    def _int_to_bytes(x, length, signed=False):
        return x.to_bytes(length, 'big', signed=signed)

    @staticmethod
    def _bytes_to_int(bts, signed=False):
        return int.from_bytes(bts, 'big', signed=signed)

    def serialize(self, obj):
        if isinstance(obj, dict):
            b = b'D'
            b += self._int_to_bytes(len(obj), 4)
            for k, v in obj.items():
                b += self.serialize(str(k))
                b += self.serialize(v)
            return b
        elif isinstance(obj, list):
            b = b'L'
            b += self._int_to_bytes(len(obj), 4)
            for x in obj:
                b += self.serialize(x)
            return b
        elif isinstance(obj, int):
            b = b'I'
            b += self._int_to_bytes(obj, 8, signed=True)
            return b
        elif isinstance(obj, str):
            s = obj.encode('utf-8')
            b = b'S'
            b += self._int_to_bytes(len(s), 4)
            b += s
            return b
        elif isinstance(obj, (datetime.datetime, datetime.date)):
            val = obj.isoformat().encode('utf-8')
            b = b'T'
            b += self._int_to_bytes(len(val), 4)
            b += val
            return b
        elif obj is None:
            return b'N'
        else:
            raise TypeError(f"Неизвестный тип: {type(obj)}")

    def deserialize(self, buf, i=0):
        def _des(j):
            if j >= len(buf):
                raise ValueError("Неожиданный конец данных :(")
            t = buf[j:j + 1]
            j += 1
            if t == b'D':
                d = {}
                n = self._bytes_to_int(buf[j:j + 4])
                j += 4
                for _ in range(n):
                    k, j = _des(j)
                    v, j = _des(j)
                    d[k] = v
                return d, j
            elif t == b'L':
                n = self._bytes_to_int(buf[j:j + 4])
                j += 4
                l = []
                for _ in range(n):
                    x, j = _des(j)
                    l.append(x)
                return l, j
            elif t == b'I':
                v = self._bytes_to_int(buf[j:j + 8], signed=True)
                j += 8
                return v, j
            elif t == b'S':
                l = self._bytes_to_int(buf[j:j + 4])
                j += 4
                v = buf[j:j + l].decode('utf-8')
                j += l
                return v, j
            elif t == b'T':
                l = self._bytes_to_int(buf[j:j + 4])
                j += 4
                val_str = buf[j:j + l].decode('utf-8')
                j += l
                try:
                    v = datetime.datetime.fromisoformat(val_str)
                except ValueError:
                    v = datetime.date.fromisoformat(val_str)
                return v, j
            elif t == b'N':
                return None, j
            else:
                raise ValueError(f"Неизвестный тип: {t}")
        result, _ = _des(i)
        return result
