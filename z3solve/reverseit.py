from z3 import *

TARGET = 315525

for length in range(10, 26):
    solver = Solver()
    chars = [BitVec(f'ch{i}', 8) for i in range(length)]
    for ch in chars:
        solver.add(ch >= 32, ch <= 126)

    result = BitVecVal(0, 32)
    for i in range(length):
        c_ext = ZeroExt(24, chars[i])
        idx = BitVecVal(i, 32)
        contrib = ((c_ext * c_ext) + (c_ext * (100 - i)) + idx + (c_ext * 7) + ((c_ext | idx) & (idx + 3))) - URem(c_ext * c_ext, idx + 1)
        result += contrib

    solver.add(result == TARGET)
    print(f"Trying length {length}")
    if solver.check() == sat:
        m = solver.model()
        s = ''.join([chr(m[ch].as_long()) for ch in chars])
        print("Valid input string:", s)
        break
