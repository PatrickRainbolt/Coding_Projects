class SAP3Interpreter:
    def __init__(self):
        # Initialize memory, registers, flags, and program counter
        self.memory = [0] * 512  # 512 bytes memory
        self.registers = [0] * 16  # 16 general-purpose registers (R0-R15)
        self.accumulator = 0  # Accumulator register
        self.pc = 0  # Program counter
        self.sp = 511  # Stack pointer (start at the end of memory)
        self.halt = False  # Halt flag
        
        # Initialize flags
        self.flags = {
            'Carry': False,
            'Zero': False,
        }

        # for Troubleshooting the code!
        self.DEBUG = False  # SYNTAX:  True or False"
		
        # Initialize labels (empty dictionary)
        self.labels = {}
        
        # Instruction set with their implementations
        self.instructions = {
            # --- 1. No Operation ---
            'NOP': self.nop,  # No operation, moves to next instruction...............SYNTAX: NOP

            # --- 2. Memory Operations ---
            'LDA': self.lda,   # Load value from memory to accumulator.................SYNTAX: LDA 0x50
            'STA': self.sta,   # Store accumulator value in memory.....................SYNTAX: STA 0x50
            'LDR': self.ldr,   # Load value from memory to register....................SYNTAX: LDR R1, 0x50
            'STR': self.str,   # Store register value to memory........................SYNTAX: STR R1, 0x50

            # --- 3. Register  and Accumulator Operations ---
            'LDRI': self.ldri, # Load immediate value to register......................SYNTAX: LDRI R1, 10
            'LDI': self.ldi,   # Load immediate value to accumulator...................SYNTAX: LDI 10
            'MOV': self.mov,   # Move value between registers or accumulator...........SYNTAX: MOV R1, R2    (Source, Destination)
        
            # --- 4. Arithmetic and Logical Operations ---
            'ADD': self.add,   # Add register value to accumulator.....................SYNTAX: ADD R1
            'SUB': self.sub,   # Subtract memory value from accumulator................SYNTAX: SUB 0x50
            'AND': self.and_op,# Logical AND with accumulator and memory...............SYNTAX: AND 0x50
            'OR': self.or_op,  # Logical OR with accumulator and memory................SYNTAX: OR 0x50
            'XOR': self.xor_op,# Logical XOR with accumulator and memory...............SYNTAX: XOR 0x50

            # --- 5. Jump and Branch Operations ---
            'JMP': self.jmp,   # Jump to specified label...............................SYNTAX: JMP LOOP
            'JG': self.jg,     # Jump to label if accumulator is greater than zero.....SYNTAX: JG <label> 
            'JZ': self.jz,     # Jump if zero flag is set..............................SYNTAX: JZ DONE
            'JNZ': self.jnz,   # Jump if zero flag is not set..........................SYNTAX: JNZ LOOP
            'JC': self.jc,     # Jump if carry flag is set.............................SYNTAX: JC CARRY_LABEL
            'JNC': self.jnc,   # Jump if carry flag is not set.........................SYNTAX: JNC NO_CARRY

            # --- 6. Arithmetic Modifications ---
            'CMA': self.cma,   # Complement accumulator (bitwise NOT)..................SYNTAX: CMA
            'INC': self.inc,   # Increment accumulator by 1............................SYNTAX: INC
            'DEC': self.dec,   # Decrement accumulator by 1............................SYNTAX: DEC
            'RAL': self.ral,   # Rotate accumulator left...............................SYNTAX: RAL
            'RAR': self.rar,   # Rotate accumulator right..............................SYNTAX: RAR

            # --- 7. I/O Operations ---
            'INP': self.inp,   # Input value to accumulator (placeholder)..............SYNTAX: INP
            'OUT': self.out,   # Output value of accumulator...........................SYNTAX: OUT

            # --- 8. Program Control ---
            'HLT': self.hlt,   # Halt the program execution............................SYNTAX: HLT

            # --- 9. Stack Operations ---
            'PUSH': self.push, # Push accumulator to stack.............................SYNTAX: PUSH
            'POP': self.pop,    # Pop value from stack to accumulator...................SYNTAX: POP

            # --- 0. For Test code or Debugging routings ---            
            'NOTE': self.note  # Prints Notes to screen. Not part of the Assembler.....SYNTAX: NOTE "String to Print"
        }

    # Sample operation implementations for instructions
    def ldr(self, args):
        """Load a value from memory into a register."""
        reg = int(args[0][1])  # Convert register name like 'R1' to integer 1
        address = int(args[1], 16)  # Convert the memory address from hexadecimal to integer
        self.registers[reg] = self.memory[address]
        return False

    def push(self, args):
        """Push the value from the accumulator to the stack (memory)"""
        self.memory[self.sp] = self.accumulator
        self.sp -= 1  # Move the stack pointer down (towards lower memory addresses)
        return False

    # Implement the POP method (Pop a value from the stack into the accumulator)
    def pop(self, args):
        """Pop a value from the stack (memory) into the accumulator"""
        self.sp += 1  # Move the stack pointer up (towards higher memory addresses)
        self.accumulator = self.memory[self.sp]
        self.zero_flag = (self.accumulator == 0)
        return False

    def mov(self, args):
        # Move value from one register to another or to/from accumulator (A)   SYNTAX: Source, Destination
        if len(args) < 2:
            self.halt = True
            return False

        try:
            # Check if moving to or from the accumulator
            if args[1] == 'A':
                # Moving value from register to accumulator
                if not args[0].startswith('R'):
                    self.halt = True
                    return False
                src_reg = int(args[0][1:])  # Convert register name like 'R1' to integer 1
                if src_reg < 0 or src_reg > 15:
                    self.halt = True    
                    return False
                # Move value from register to accumulator
                self.accumulator = self.registers[src_reg]

            elif args[0] == 'A':
                # Moving value from accumulator to a register
                if not args[1].startswith('R'):
                    self.halt = True    
                    return False
                dest_reg = int(args[1][1:])  # Convert register name like 'R1' to integer 1
                if dest_reg < 0 or dest_reg > 15:
                    self.halt = True    
                    return False
                # Move value from accumulator to register
                self.registers[dest_reg] = self.accumulator

            else:
                # Regular register-to-register move
                if not args[0].startswith('R') or not args[1].startswith('R'):
                    self.halt = True
                    return False

                src_reg = int(args[0][1:])  # Convert register name like 'R1' to integer 1
                dest_reg = int(args[1][1:])  # Convert register name like 'R2' to integer 2    

                # Check if the registers are valid (between 0-15 for R0 to R15)
                if src_reg < 0 or src_reg > 15 or dest_reg < 0 or dest_reg > 15:
                    self.halt = True    
                    return False    

                # Perform the move
                if self.DEBUG: print(f"MOV: R{src_reg}[{self.registers[src_reg]}] to R{dest_reg}[{self.registers[dest_reg]}]")
                self.registers[dest_reg] = self.registers[src_reg]

        except (ValueError, IndexError) as e:
            self.halt = True
            return False

        return False

    def nop(self, args):
        """No operation, just move to the next instruction."""
        return False

    def lda(self, args):
        """Load into the accumulator from memory."""
        address = int(args[0], 16)
        self.accumulator = self.memory[address]
        self.zero_flag = (self.accumulator == 0)
        return False

    def sta(self, args):
        """Store the accumulator into the specified memory address."""
        if self.DEBUG: print(f"STA: args {args}")
        if len(args) != 1:
            print(f"Error: STA requires one argument (memory address), but got {len(args)}")
            self.halt = True
            return False

        # Check if the argument is a valid memory address (could be in hexadecimal or decimal)
        try:
            # Handle hexadecimal addresses (e.g., 0x00, 0xFF)
            address = int(args[0], 16)  # This allows both decimal and hexadecimal input
            if address < 0 or address >= 512:
                print(f"Error: Address {address} out of range.")
                self.halt = True
                return False
        except ValueError:
            print(f"Error: Invalid memory address {args[0]} for STA instruction.")
            self.halt = True
            return False

        # Store the value in the accumulator (A) into the specified memory address
        self.memory[address] = self.accumulator
        if self.DEBUG: print(f"STA: Stored value {self.accumulator} into memory address {address}")
    
        return False

    def add(self, args):
        """Add value from a register or memory address to the accumulator."""
        if len(args) != 1:
            print(f"Error: ADD requires one argument, but got {len(args)}")
            self.halt = True
            return False

        try:
            # Check if the argument is a register (e.g., R0, R1, etc.)
            if args[0].startswith('R'):
                reg = int(args[0][1])  # Extract register index from 'R0', 'R1', etc.
                if reg < 0 or reg > 15:
                    print(f"Error: Register out of range. Registers should be between R0 and R15.")
                    self.halt = True
                    return False
                # Add the value from the specified register to the accumulator
                self.accumulator += self.registers[reg]
        
            # Check if the argument is a memory address (e.g., 0x00, 0x02, etc.)
            else:
                address = int(args[0], 16)  # Convert the memory address (e.g., 0x02) from hex to decimal
                if address < 0 or address >= 512:
                    print(f"Error: Address {address} out of range.")
                    self.halt = True
                    return False
                # Add the value from memory at the specified address to the accumulator
                self.accumulator += self.memory[address]

            # Check for overflow (if the accumulator exceeds the max value for an 8-bit number)
            if self.accumulator > 255:
                self.accumulator -= 255  # Wrap around the 8-bit value
                self.flags['Carry'] = True  # Set the Carry flag
            else:
                self.flags['Carry'] = False  # Clear the Carry flag

            # Check if the accumulator is zero (for Zero flag)
            if self.accumulator == 0:
                self.flags['Zero'] = True
            else:
                self.flags['Zero'] = False

        except (ValueError, IndexError) as e:
            print(f"Error processing ADD instruction: {e}")
            self.halt = True
            return False

        return False


    def sub(self, args):
        """Subtract a value from memory from the accumulator."""
        address = int(args[0], 16)
        self.accumulator -= self.memory[address]
        self.zero_flag = (self.accumulator == 0)
        return False

    def and_op(self, args):
        """Logical AND operation on accumulator and value from memory."""
        address = int(args[0], 16)
        self.accumulator &= self.memory[address]
        self.zero_flag = (self.accumulator == 0)
        return False

    def or_op(self, args):
        """Logical OR operation on accumulator and value from memory."""
        address = int(args[0], 16)
        self.accumulator |= self.memory[address]
        self.zero_flag = (self.accumulator == 0)
        return False

    def xor_op(self, args):
        """Logical XOR operation on accumulator and value from memory."""
        address = int(args[0], 16)
        self.accumulator ^= self.memory[address]
        self.zero_flag = (self.accumulator == 0)
        return False

    def jg(self, label):
        """Jump to label if accumulator is greater than zero"""
        if isinstance(label, list):
            label = label[0]  # Ensure label is a string, not a list

        if label in self.labels:  # Assuming you have a dictionary of labels
            self.pc = self.labels[label] - 1 # Set program counter to the label's address
        else:
            print(f"Label {label} not found!")

    def jmp(self, args):
        """Jump to a specific label in the program."""
        label = args[0]
        if label in self.labels:
            self.pc = self.labels[label]
        else:
            print(f"Error: Label {label} not found.")
            self.halt = True
        return True  # Jump modifies PC directly

    def jz(self, args):
        """Jump if zero flag is set."""
        if self.zero_flag:
            self.jmp(args)
        else:
            return False
        return True

    def jnz(self, args):
        """Jump if zero flag is not set."""
        if not self.zero_flag:
            self.jmp(args)
        else:
            return False
        return True

    def jc(self, args):
        """Jump if Carry flag is set."""
        if len(args) != 1:
            print(f"Error: JC requires one argument (label), but got {len(args)}")
            self.halt = True
            return False
    
        label = args[0]  # The label to jump to
    
        if self.flags['Carry']:  # Check the Carry flag in the flags dictionary
            if label in self.labels:
                self.pc = self.labels[label]  # Set the program counter to the label address    
                if self.DEBUG: print(f"JC: Jumping to label {label} (Address {self.pc})")
            else:
                print(f"Error: Label {label} not found.")
                self.halt = True
                return False
        else:
            print(f"JC: No jump, Carry flag is not set.")
    
        return False

    def jnc(self, args):
        """Jump if carry flag is not set."""
        if not self.carry_flag:
            self.jmp(args)
        else:
            return False
        return True

    def cma(self, args):
        """Complement the accumulator."""
        self.accumulator = ~self.accumulator & 0xFF
        self.zero_flag = (self.accumulator == 0)
        return False

    def inc(self, args):
        """Increment the accumulator."""
        self.accumulator += 1
        self.accumulator &= 0xFF  # Keep the value within byte size
        self.zero_flag = (self.accumulator == 0)
        return False

    def dec(self, args):
        """Decrement the accumulator."""
        self.accumulator -= 1
        self.accumulator &= 0xFF  # Keep the value within byte size
        self.zero_flag = (self.accumulator == 0)
        return False

    def ral(self, args):
        """Rotate accumulator left."""
        self.accumulator = ((self.accumulator << 1) & 0xFF) | (self.accumulator >> 7)
        self.zero_flag = (self.accumulator == 0)
        return False

    def rar(self, args):
        """Rotate accumulator right."""
        self.accumulator = (self.accumulator >> 1) | ((self.accumulator & 1) << 7)
        self.zero_flag = (self.accumulator == 0)
        return False

    def inp(self, args):
        """Input value (simulated as zero for now)."""
        self.accumulator = 0  # Placeholder for actual input
        self.zero_flag = (self.accumulator == 0)
        return False

    def out(self, args):
        """Output the value of a register or memory."""
        if args:  # If there are arguments, output the value of the register
            reg = args[0]  # Get the register name, e.g., "R0"
            reg_num = int(reg[1:])  # Convert "R0" to 0, "R1" to 1, etc.

            if 0 <= reg_num <= 15:  # Ensure valid register range
                print(f"Output: {self.registers[reg_num]}")
            else:
                print(f"Error: Invalid register {reg}")
        else:
            print(f"Output: {self.accumulator}")  # If no argument, print accumulator
        return False

    def hlt(self, args):
        """Halt the program."""
        self.halt = True
        return False

    def str(self, args):
        """Store register to memory"""
        if len(args) < 2:
            print("Error: STR requires two arguments (register, address)")
            self.halt = True
            return False
            
        reg, addr = args[0], args[1]
        try:
            reg_num = int(reg[1:])  # Extract the register number (e.g., R0 -> 0)
            address = self.parse_address(addr)  # Convert the address to integer
            self.memory[address] = self.registers[reg_num] # Store the value of the register in memory
        except (ValueError, IndexError):
            print(f"Error: Invalid arguments for STR: {reg}, {addr}")
            self.halt = True
            return False
            
        return False
    
    def ldri(self, args):
        """Load register immediate"""
        if len(args) < 2:
            #print("Error: LDRI requires two arguments (register, value)")
            self.halt = True
            return False

        try:
            reg, value = args[0], args[1]
            reg_num = int(reg[1:])
            int_value = int(value) & 0xFF  # Ensure value is a byte (0-255)

            # Check that the register is valid (0-15 for R0 to R15)
            if reg_num < 0 or reg_num > 15:
                print(f"Error: Invalid register number {reg_num}. Registers should be between R0 and R15.")
                self.halt = True
                return False

            self.registers[reg_num] = int_value
            #print(f"LDRI: Loaded value {int_value} into R{reg_num}")

        except (ValueError, IndexError) as e:
            print(f"Error processing LDRI instruction: {e}")
            self.halt = True
            return False

        return False

    def ldi(self, args):
        """Load Immediate value into register."""
        if len(args) != 2:
            print(f"Error: LDI requires two arguments (register, value), but got {len(args)}")    
            self.halt = True
            return False

        try:
            reg = int(args[0][1:])  # Convert register name like 'R0' to integer 0, 'R8' to 8, 'R10' to 10
            value = int(args[1])    # Convert the immediate value to an integer

            # Check if the register is valid (0-15 for R0 to R15)
            if reg < 0 or reg > 15:
                print(f"Error: Invalid register number {reg}. Registers should be between R0 and R15.")
                self.halt = True
                return False

            # Load the immediate value into the specified register
            self.registers[reg] = value
            if self.DEBUG: print(f"LDI: Loaded immediate value {value} into R{reg}")

        except (ValueError, IndexError) as e:
            print(f"Error processing LDI instruction: {e}")
            self.halt = True
            return False

        return False

    def note(self, args):
        """Print a message to the screen for debugging purposes, with dynamic values from registers, accumulator, and memory."""

        if len(args) < 1:
            print("Error: NOTE command requires a string argument.")
            self.halt = True
            return False

        message = ' '.join(args)  # Join all arguments into a single string (in case the message has spaces)

        if '{' in message and '}' in message:    # If message contains placeholders 

            # Replace placeholders for registers R0 to R15 and A (accumulator)
            for i in range(16):  # For registers R0 to R15
                #print(f"FOR: [{self.registers[i]}]")
                message = message.replace(f"{{R{i}}}", str(self.registers[i]))
    
            # Replace the placeholder for the accumulator (A)
            message = message.replace("{A}", str(self.accumulator))

            # Replace placeholders for memory locations like {0x01}, {0x02}, ..., dynamically
            # We will look for patterns like {0x01}, {0x02}, and replace them with corresponding memory values
            for i in range(16):  # This example assumes memory is 16 locations, you can expand it if needed
                message = message.replace(f"{{0x{i:02X}}}", str(self.memory[i]))  # Format as {0x01}, {0x02}, etc.

        print(f"Note  :------------------{message}")  # Print the message with a "NOTE" prefix for clarity
        return False

    # Method to parse the program from a file
    def parse_program(self, filename):
        """Parse a SAP-3 ASM file"""
        with open(filename, 'r') as f:
            lines = f.readlines()
    
        # First pass: collect labels
        line_num = 0
        self.program = []

        for line in lines:
            # Remove comments and trim whitespace
            if ';' in line:
                line = line[:line.index(';')]
            line = line.strip()

            # Skip empty lines
            if not line:
                continue    

            # Check for labels
            if ':' in line and not line.lstrip().startswith("NOTE"):
                label, rest = line.split(':', 1)
                label = label.strip()
                self.labels[label] = line_num
                line = rest.strip()


                # If there's nothing after the label, continue
                if not line:
                    continue    

            # Add to program
            if line:  # Make sure line isn't empty after removing label
                self.program.append(line) 
                if self.DEBUG: print(f"Added to program: {line.strip()} at address {line_num}")  # Debugging message   
                line_num += 1

    def parse_address(self, addr):
        """Parse an address and return it as an integer."""
        if addr.startswith('0x'):
            # If the address is in hexadecimal format (e.g., 0x00, 0x1F), convert it to an integer
            return int(addr, 16)
        else:
            # If the address is just a number (e.g., 5), return it as an integer
            return int(addr)

    def execute_program(self):
        """Execute the loaded program"""
        self.pc = 0
        while self.pc < len(self.program) and not self.halt:
            line = self.program[self.pc]
            if self.DEBUG: print(f"\nExecuting line {self.pc}: {line}")  # Add debug print here

            # Skip label lines
            if ':' in line:
                label, rest = line.split(':', 1)
                label = label.strip()
                if label in self.labels:
                    if self.DEBUG: print(f"Label found: {label}, skipping instruction line.")
                    self.pc += 1
                    continue

            # Parse instruction and arguments
            parts = line.split(None, 1)  # Split on first whitespace    
            opcode = parts[0].upper()
            args = []

            if len(parts) > 1 and parts[1].strip():
                # Process arguments    
                args_str = parts[1].strip()
                if ',' in args_str:
                    args = [arg.strip() for arg in args_str.split(',')]
                else:
                    args = [args_str.strip()]

            if self.DEBUG: print(f"Parsed opcode: {opcode}, args: {args}")  # Add debug print here
    
            # Handle NOTE instructions separately
            if opcode == "NOTE":
                # For NOTE instruction, pass the args to the note function
                self.note(args)
                self.pc += 1
            elif opcode in self.instructions:
                # Execute other instructions normally
                if self.DEBUG: print(f"Executing instruction: {opcode} with arguments {args}")
                pc_modified = self.instructions[opcode](args)
                if not pc_modified:
                    self.pc += 1
            else:
                # Handle unknown instructions
                print(f"Unknown instruction: {opcode}")
                self.halt = True


    def display_state(self):
        """Display the current state of the interpreter"""
        print(f"\nAccumulator: {self.accumulator} (0x{self.accumulator:02X})")
        print(f"PC: {self.pc}, SP: {self.sp}")
        print(f"Flags - Zero: {self.flags['Zero']}, Carry: {self.flags['Carry']}")  # Fixed here

        print("\nRegisters:")
        # Loop over the range of 4 columns
        for i in range(4):
            # Loop over the registers and print them in a column-based format
            for j in range(i, 16, 4):
                print(f"R{j:02}: {self.registers[j]:3}  (0x{self.registers[j]:02X})", end="  ")
            print()  # New line after each row of 4 registers

        print("\nMemory (non-zero values):")
        for i in range(0, 512, 16):
            row_has_data = any(self.memory[i + j] != 0 for j in range(16))
            if row_has_data:
                print(f"{i:03X}:", end=" ")
                for j in range(16):
                    print(f"{self.memory[i + j]:02X}", end=" ")
                print()
        print()

def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python sap3_interpreter.py <asm_file>")
        return

    interpreter = SAP3Interpreter()
    interpreter.parse_program(sys.argv[1])

    print(f"Loaded program with {len(interpreter.program)} instructions")
    print("Labels:", interpreter.labels)
    print("\nStarting execution...")

    interpreter.execute_program()

    print("\nProgram execution completed")
    interpreter.display_state()

if __name__ == "__main__":
    main()

