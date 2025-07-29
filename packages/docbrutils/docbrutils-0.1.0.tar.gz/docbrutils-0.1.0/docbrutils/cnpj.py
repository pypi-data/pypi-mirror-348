
import re
from random import randint

def validate_cnpj(cnpj: str) -> bool:
    cnpj = re.sub(r'\D', '', cnpj)
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    def calc_digit(digs, weights):
        s = sum(int(d) * w for d, w in zip(digs, weights))
        d = 11 - s % 11
        return '0' if d >= 10 else str(d)

    w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    w2 = [6] + w1
    d1 = calc_digit(cnpj[:12], w1)
    d2 = calc_digit(cnpj[:12] + d1, w2)
    return cnpj.endswith(d1 + d2)

def generate_cnpj() -> str:
    base = [randint(0, 9) for _ in range(12)]
    d1 = _calculate_digit(base, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    d2 = _calculate_digit(base + [int(d1)], [6] + [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    return ''.join(map(str, base + [int(d1), int(d2)]))

def _calculate_digit(numbers, weights):
    s = sum(x * y for x, y in zip(numbers, weights))
    r = 11 - s % 11
    return 0 if r >= 10 else r
