def hamming74_decode(_codeword):
    bits = [int(ch) for ch in _codeword]
    if len(bits) != 7 or any(b not in [0, 1] for b in bits):
        raise ValueError("Ввод должен содержать ровно 7 цифр 0 или 1")

    positions = ["r₁", "r₂", "i₁", "r₃", "i₂", "i₃", "i₄"]
    r1, r2, i1, r3, i2, i3, i4 = bits

    s1 = r1 ^ i1 ^ i2 ^ i4
    s2 = r2 ^ i1 ^ i3 ^ i4
    s3 = r3 ^ i2 ^ i3 ^ i4

    syndrome = (s3 << 2) | (s2 << 1) | s1

    bits_corrected = bits[:]
    _error_position, _error_bit = None, None
    if syndrome != 0:
        idx = syndrome - 1
        _error_position = syndrome
        _error_bit = positions[idx]
        bits_corrected[idx] ^= 1

    _info_bits = [bits_corrected[2], bits_corrected[4], bits_corrected[5], bits_corrected[6]]

    return _info_bits, _error_bit, _error_position

if __name__ == '__main__':
    codeword = input('Введите кодовое слово (7 бит, например 1011001): ').strip()
    info_bits, error_bit, error_position = hamming74_decode(codeword)
    if error_position:
        print(f"Обнаружена ошибка в бите {error_bit} (№ {error_position}). Исправлено.")
    else:
        print("Ошибок не обнаружено.")
    print("Правильное сообщение (информационные биты):", ''.join(map(str, info_bits)))
