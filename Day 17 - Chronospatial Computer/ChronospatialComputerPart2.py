
def parse_input(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip() != '']

    # Example lines:
    # ["Register A: 60589763", "Register B: 0", "Register C: 0", "Program: 2,4,1,5,7,..."]

    regA = int(lines[0].split(':')[1].strip())
    regB = int(lines[1].split(':')[1].strip())
    regC = int(lines[2].split(':')[1].strip())

    prog_str = lines[3].split(':', 1)[1].strip()
    program = [int(x.strip()) for x in prog_str.split(',')]

    return regA, regB, regC, program

def combo_value(op, A, B, C):
    # Combo operand mapping: 0-3 = literal 0-3, 4=A, 5=B, 6=C, 7 invalid
    if op < 4:
        return op
    elif op == 4:
        return A
    elif op == 5:
        return B
    elif op == 6:
        return C
    else:
        raise ValueError("Invalid combo operand (7 encountered).")

def run_program(A_init, B_init, C_init, program):
    A, B, C = A_init, B_init, C_init
    ip = 0
    output_values = []
    length = len(program)

    while ip < length:
        opcode = program[ip]
        if ip + 1 >= length:
            # No operand available, halt
            break
        operand = program[ip+1]

        ip_next = ip + 2

        if opcode == 0:
            # adv: A = A // (2^(combo_value))
            val = combo_value(operand, A, B, C)
            A = A >> val  # Using bit shift for division by powers of two
        elif opcode == 1:
            # bxl: B = B XOR literal_operand
            B = B ^ operand
        elif opcode == 2:
            # bst: B = combo_value % 8
            val = combo_value(operand, A, B, C)
            B = val & 7  # x % 8 is x & 7 for nonnegative integers
        elif opcode == 3:
            # jnz: if A != 0, ip = literal_operand
            if A != 0:
                ip_next = operand
        elif opcode == 4:
            # bxc: B = B XOR C (operand ignored)
            B = B ^ C
        elif opcode == 5:
            # out: output combo_value % 8
            val = combo_value(operand, A, B, C)
            output_values.append(val & 7)
        elif opcode == 6:
            # bdv: B = A // (2^(combo_value))
            val = combo_value(operand, A, B, C)
            B = A >> val
        elif opcode == 7:
            # cdv: C = A // (2^(combo_value))
            val = combo_value(operand, A, B, C)
            C = A >> val
        else:
            # Invalid opcode
            break

        ip = ip_next

    return output_values

def solve_part2(program, B_init=0, C_init=0):
    # Backward search for initial A
    reversed_instructions = list(reversed(program))
    candidates = [0]

    for instruction in reversed_instructions:
        new_candidates = []
        for candidate in candidates:
            shifted = candidate << 3
            # Check attempts from shifted to shifted+8 inclusive
            for attempt in range(shifted, shifted + 9):
                output_values = run_program(attempt, B_init, C_init, program)
                if output_values and output_values[0] == instruction:
                    new_candidates.append(attempt)
        candidates = new_candidates
        if not candidates:
            # No candidates found means no solution at this stage
            break

    # The first candidate (lowest) in the resulting list is the solution
    return candidates[0] if candidates else None

def main():
    # Read input
    original_A, B_init, C_init, program = parse_input('input.txt')
    # According to the puzzle, we ignore the original_A and find a new one.
    result = solve_part2(program, B_init, C_init)
    if result is not None:
        print(result)
    else:
        print("No solution found")

if __name__ == "__main__":
    main()
