def main():
    # Read the input from input.txt
    with open('input.txt', 'r') as f:
        lines = f.read().strip().split('\n')
    
    # Parse the registers
    # Expected lines like "Register A: 729"
    A = int(lines[0].split(':')[1].strip())
    B = int(lines[1].split(':')[1].strip())
    C = int(lines[2].split(':')[1].strip())
    
    # Parse the program
    # Expected line like "Program: 0,1,5,4,3,0"
    program_line = lines[3].split(':')[1].strip()
    program = [int(x.strip()) for x in program_line.split(',')]
    
    # Define a helper to get combo operand value
    def get_combo_value(op):
        # combo operands:
        # 0-3 => literal 0-3
        # 4 => value of A
        # 5 => value of B
        # 6 => value of C
        # 7 => reserved, won't appear
        if op <= 3:
            return op
        elif op == 4:
            return A
        elif op == 5:
            return B
        elif op == 6:
            return C
        else:
            raise ValueError("Invalid combo operand encountered.")
    
    # The instructions modify A, B, C or may jump/output as described.
    # instruction pointer
    ip = 0
    output_values = []
    
    # Run until we try to read opcode past the end of program
    while ip < len(program):
        opcode = program[ip]
        # If next operand doesn't exist, we halt as well
        if ip+1 >= len(program):
            # No operand available, halt.
            break
        operand = program[ip+1]
        
        if opcode == 0:  # adv
            # A = floor(A / 2^(combo_value))
            val = get_combo_value(operand)
            divisor = 2 ** val
            A = A // divisor
            ip += 2
            
        elif opcode == 1:  # bxl
            # B = B XOR literal_operand
            # operand is literal here
            B = B ^ operand
            ip += 2
            
        elif opcode == 2:  # bst
            # B = (combo_value % 8)
            val = get_combo_value(operand)
            B = val % 8
            ip += 2
            
        elif opcode == 3:  # jnz
            # If A != 0, ip = literal_operand
            # else ip += 2
            if A != 0:
                ip = operand
            else:
                ip += 2
                
        elif opcode == 4:  # bxc
            # B = B XOR C
            # operand is ignored
            B = B ^ C
            ip += 2
            
        elif opcode == 5:  # out
            # output combo_value % 8
            val = get_combo_value(operand)
            output_values.append(val % 8)
            ip += 2
            
        elif opcode == 6:  # bdv
            # B = floor(A / 2^(combo_value))
            val = get_combo_value(operand)
            divisor = 2 ** val
            B = A // divisor
            ip += 2
            
        elif opcode == 7:  # cdv
            # C = floor(A / 2^(combo_value))
            val = get_combo_value(operand)
            divisor = 2 ** val
            C = A // divisor
            ip += 2
            
        else:
            # Invalid opcode
            break
    
    # Print the output values separated by commas
    print(','.join(map(str, output_values)))

if __name__ == "__main__":
    main()
