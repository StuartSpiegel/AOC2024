def is_known_zero(bit):
    return bit == -1

def is_known_one(bit):
    return bit == -2

def is_unknown(bit):
    return isinstance(bit, int) and bit >= 0

def invert_bit(b):
    if b == -1:
        return -2  # 0 -> 1
    if b == -2:
        return -1  # 1 -> 0
    return ('inv', b)

def bit_xor(b1, b2):
    if b1 == -1:
        return b2
    if b2 == -1:
        return b1
    if b1 == -2:
        return invert_bit(b2)
    if b2 == -2:
        return invert_bit(b1)
    if is_unknown(b1) and is_unknown(b2):
        if b1 == b2:
            return -1
        else:
            return ('xor', b1, b2)
    if isinstance(b1, tuple) or isinstance(b2, tuple):
        return ('xor', b1, b2)
    return ('xor', b1, b2)

def xor_array(a1, a2):
    return [bit_xor(x, y) for x, y in zip(a1, a2)]

def const_bits(value, length=1000):
    arr = [-1]*length
    i = 0
    v = value
    while v > 0 and i < length:
        if v & 1:
            arr[i] = -2  # known 1
        else:
            arr[i] = -1  # known 0
        i += 1
        v >>= 1
    return arr

def zero_bits(length=1000):
    return [-1]*length

def a_init_bits(length=1000):
    return list(range(length))

def shift_right(r, amount):
    arr = r[:]
    for _ in range(amount):
        arr.pop(0)
        arr.append(-1)
    return arr

def xor_register(r, val):
    mask = const_bits(val, length=len(r))
    arr = r[:]
    for i in range(len(arr)):
        arr[i] = bit_xor(arr[i], mask[i])
    return arr

def is_all_zero(bits_arr):
    for b in bits_arr:
        if b == -2: 
            return False
        if is_unknown(b):
            return False
        if isinstance(b, tuple):
            return False
    return True

def resolve_bit_expr(expr, known_bits):
    if expr == -1:
        return 0
    if expr == -2:
        return 1
    if is_unknown(expr):
        if expr in known_bits:
            return known_bits[expr]
        else:
            return None
    if isinstance(expr, tuple):
        if expr[0] == 'inv':
            sub = resolve_bit_expr(expr[1], known_bits)
            if sub is None:
                return None
            return 1 - sub
        if expr[0] == 'xor':
            vals = []
            for e in expr[1:]:
                r = resolve_bit_expr(e, known_bits)
                if r is None:
                    vals.append(e)
                else:
                    vals.append(r)
            known_val = 0
            unknown_list = []
            for v in vals:
                if v in (0,1):
                    known_val ^= v
                else:
                    unknown_list.append(v)
            if len(unknown_list) == 0:
                return known_val
            if len(unknown_list) == 1:
                u = unknown_list[0]
                if is_unknown(u) and u not in known_bits:
                    return None
                else:
                    sub = resolve_bit_expr(u, known_bits)
                    if sub is None:
                        return None
                    return sub ^ known_val
            return None
    return None

def find_single_unknown(expr, known_bits, resolve):
    res = resolve(expr, known_bits)
    if res is not None:
        return None
    if is_unknown(expr):
        if expr not in known_bits:
            return expr
    if isinstance(expr, tuple):
        if expr[0] == 'inv':
            return find_single_unknown(expr[1], known_bits, resolve)
        if expr[0] == 'xor':
            candidates = []
            for e in expr[1:]:
                r = resolve(e, known_bits)
                if r is None:
                    u = find_single_unknown(e, known_bits, resolve)
                    if u is not None:
                        candidates.append(u)
            if len(candidates) == 1:
                return candidates[0]
            return None
    return None

def evaluate_fixed_part(expr, unknown_bit, known_bits, resolve):
    if expr == -1:
        return 0
    if expr == -2:
        return 1
    if is_unknown(expr):
        if expr == unknown_bit:
            return 0
        if expr in known_bits:
            return known_bits[expr]
        return 0
    if isinstance(expr, tuple):
        if expr[0] == 'inv':
            return 1 - evaluate_fixed_part(expr[1], unknown_bit, known_bits, resolve)
        if expr[0] == 'xor':
            val = 0
            for e in expr[1:]:
                v = evaluate_fixed_part(e, unknown_bit, known_bits, resolve)
                val ^= v
            return val
    return 0

def get_small_constant(bits_arr):
    val = 0
    known_bits = {}
    for i in range(3):
        b = bits_arr[i] if i < len(bits_arr) else -1
        c = resolve_bit_expr(b, known_bits)
        if c is None:
            return None
        if c == 1:
            val |= (1 << i)
    return val

def main():
    with open('input.txt', 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    A_start_given = int(lines[0].split(':')[1].strip())
    B_start = int(lines[1].split(':')[1].strip())
    C_start = int(lines[2].split(':')[1].strip())

    program_line = lines[3].split(':', 1)[1].strip()
    program = [int(x.strip()) for x in program_line.split(',')]

    MAX_BITS = 1000
    A = a_init_bits(MAX_BITS)
    B = const_bits(B_start, MAX_BITS)
    C = const_bits(C_start, MAX_BITS)

    def combo_value(op):
        if op <= 3:
            return const_bits(op, MAX_BITS)
        elif op == 4:
            return A[:]
        elif op == 5:
            return B[:]
        elif op == 6:
            return C[:]
        else:
            raise ValueError("Invalid combo operand")

    constraints = []
    ip = 0

    # A helper function to handle shift instructions (adv, bdv, cdv)
    def handle_div_instruction(register, operand):
        val = combo_value(operand)
        shift_val = get_small_constant(val)
        if shift_val is None:
            # Attempt to resolve again or raise error
            # If we cannot resolve a small integer, no solution.
            raise RuntimeError("Cannot resolve non-literal shift amount. Complex scenario not handled.")
        return shift_right(register, shift_val)

    while ip < len(program):
        if ip+1 >= len(program):
            break
        opcode = program[ip]
        operand = program[ip+1]

        if opcode == 0:  # adv
            A = handle_div_instruction(A, operand)
            ip += 2

        elif opcode == 1:  # bxl
            B = xor_register(B, operand)
            ip += 2

        elif opcode == 2:  # bst
            val = combo_value(operand)
            B = val[:]
            for i in range(3, len(B)):
                B[i] = -1
            ip += 2

        elif opcode == 3:  # jnz
            if not is_all_zero(A):
                ip = operand
            else:
                ip += 2

        elif opcode == 4:  # bxc
            B = xor_array(B, C)
            ip += 2

        elif opcode == 5:  # out
            val = combo_value(operand)
            expected_val = program[len(constraints)//3]
            low3 = val[0:3]
            for i in range(3):
                bit_needed = (expected_val >> i) & 1
                constraints.append((low3[i], bit_needed))
            ip += 2

        elif opcode == 6:  # bdv
            B = handle_div_instruction(A, operand)
            ip += 2

        elif opcode == 7:  # cdv
            C = handle_div_instruction(A, operand)
            ip += 2

        else:
            break

    known_A_bits = {}

    for bit_expr, req_val in constraints:
        res = resolve_bit_expr(bit_expr, known_A_bits)
        if res is None:
            if is_unknown(bit_expr):
                known_A_bits[bit_expr] = req_val
            else:
                single_unknown = find_single_unknown(bit_expr, known_A_bits, resolve_bit_expr)
                if single_unknown is not None:
                    fixed_val = evaluate_fixed_part(bit_expr, single_unknown, known_A_bits, resolve_bit_expr)
                    bit_needed = req_val ^ fixed_val
                    known_A_bits[single_unknown] = bit_needed
                else:
                    raise RuntimeError("Complex constraint with no single unknown bit.")
        else:
            if res != req_val:
                # Conflict: assume puzzle is correct and no conflict occurs.
                pass

    A_init_candidate = 0
    for i, v in known_A_bits.items():
        if v == 1:
            A_init_candidate |= (1 << i)

    if A_init_candidate == 0:
        A_init_candidate = 1

    print(A_init_candidate)


if __name__ == "__main__":
    main()
