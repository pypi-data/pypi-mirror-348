
import re
from random import randint

def validate_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    def calc_digit(digs):
        s = sum(int(d) * f for d, f in zip(digs, range(len(digs)+1, 1, -1)))
        d = 11 - s % 11
        return '0' if d > 9 else str(d)

    d1 = calc_digit(cpf[:9])
    d2 = calc_digit(cpf[:9] + d1)
    return cpf.endswith(d1 + d2)

def generate_cpf() -> str:
    nine_digits = [randint(0, 9) for _ in range(9)]
    d1 = _calculate_digit(nine_digits)
    d2 = _calculate_digit(nine_digits + [int(d1)])
    return ''.join(map(str, nine_digits + [int(d1), int(d2)]))

def _calculate_digit(digits):
    s = sum(d * f for d, f in zip(digits, range(len(digits)+1, 1, -1)))
    d = 11 - s % 11
    return 0 if d > 9 else d
