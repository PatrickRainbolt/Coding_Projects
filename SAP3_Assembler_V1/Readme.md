# Introduction to Python 3 Interpreted Assembler

This assembler provides a simple set of instructions for low-level programming in Python. It is designed to simulate assembly-like code that can interact with registers, memory, and control structures. Below is an overview of the available instructions that can be used to write programs in this assembly language.

## 1. No Operation (NOP)
The NOP instruction performs no operation. It effectively moves to the next instruction in the program.
- **Syntax**: `NOP`

## 2. Memory Operations
These instructions allow you to load and store data from and to memory addresses.

### LDA
- **Description**: Load a value from a specific memory address into the accumulator.
- **Syntax**: `LDA <memory_address>`
- **Example**: `LDA 0x50`

### STA
- **Description**: Store the value from the accumulator into a specified memory address.
- **Syntax**: `STA <memory_address>`
- **Example**: `STA 0x50`

### LDR
- **Description**: Load a value from a specific memory address into a register.
- **Syntax**: `LDR <register>, <memory_address>`
- **Example**: `LDR R1, 0x50`

### STR
- **Description**: Store the value from a specified register into a memory address.
- **Syntax**: `STR <register>, <memory_address>`
- **Example**: `STR R1, 0x50`

## 3. Register and Accumulator Operations
These instructions manipulate the values in the registers and accumulator.

### LDRI
- **Description**: Load an immediate value into a register.
- **Syntax**: `LDRI <register>, <value>`
- **Example**: `LDRI R1, 10`

### LDI
- **Description**: Load an immediate value into the accumulator.
- **Syntax**: `LDI <value>`
- **Example**: `LDI 10`

### MOV
- **Description**: Move the value from one register or the accumulator to another register or accumulator.
- **Syntax**: `MOV <source>, <destination>`
- **Example**: `MOV R1, R2`

## 4. Arithmetic and Logical Operations
These instructions perform arithmetic and logical operations on the accumulator or registers.

### ADD
- **Description**: Add a value from a register to the accumulator.
- **Syntax**: `ADD <register>`
- **Example**: `ADD R1`

### SUB
- **Description**: Subtract a value from memory from the accumulator.
- **Syntax**: `SUB <memory_address>`
- **Example**: `SUB 0x50`

### AND
- **Description**: Perform a logical AND operation between the accumulator and a memory value.
- **Syntax**: `AND <memory_address>`
- **Example**: `AND 0x50`

### OR
- **Description**: Perform a logical OR operation between the accumulator and a memory value.
- **Syntax**: `OR <memory_address>`
- **Example**: `OR 0x50`

### XOR
- **Description**: Perform a logical XOR operation between the accumulator and a memory value.
- **Syntax**: `XOR <memory_address>`
- **Example**: `XOR 0x50`

## 5. Jump and Branch Operations
These instructions control the flow of the program by jumping to specified labels based on conditions.

### JMP
- **Description**: Jump to a specified label.
- **Syntax**: `JMP <label>`
- **Example**: `JMP LOOP`

### JG
- **Description**: Jump to a label if the accumulator is greater than zero.
- **Syntax**: `JG <label>`
- **Example**: `JG LOOP`

### JZ
- **Description**: Jump to a label if the zero flag is set (i.e., the accumulator is zero).
- **Syntax**: `JZ <label>`
- **Example**: `JZ DONE`

### JNZ
- **Description**: Jump to a label if the zero flag is not set (i.e., the accumulator is non-zero).
- **Syntax**: `JNZ <label>`
- **Example**: `JNZ LOOP`

### JC
- **Description**: Jump to a label if the carry flag is set.
- **Syntax**: `JC <label>`
- **Example**: `JC CARRY_LABEL`

### JNC
- **Description**: Jump to a label if the carry flag is not set.
- **Syntax**: `JNC <label>`
- **Example**: `JNC NO_CARRY`

## 6. Arithmetic Modifications
These instructions modify the value of the accumulator.

### CMA
- **Description**: Complement the accumulator (bitwise NOT).
- **Syntax**: `CMA`

### INC
- **Description**: Increment the accumulator by 1.
- **Syntax**: `INC`

### DEC
- **Description**: Decrement the accumulator by 1.
- **Syntax**: `DEC`

### RAL
- **Description**: Rotate the accumulator left.
- **Syntax**: `RAL`

### RAR
- **Description**: Rotate the accumulator right.
- **Syntax**: `RAR`

## 7. I/O Operations
These instructions are for input and output operations.

### INP
- **Description**: Input a value into the accumulator (currently a placeholder for future I/O functionality).
- **Syntax**: `INP`

### OUT
- **Description**: Output the value of the accumulator.
- **Syntax**: `OUT`

## 8. Program Control

### HLT
- **Description**: Halt the program execution.
- **Syntax**: `HLT`

## 9. Stack Operations

### PUSH
- **Description**: Push the value of the accumulator onto the stack.
- **Syntax**: `PUSH`

### POP
- **Description**: Pop a value from the stack into the accumulator.
- **Syntax**: `POP`

## 10. Test/Debugging

### NOTE
- **Description**: Prints a note or message to the screen (used for debugging purposes).
- **Syntax**: `NOTE "<message>"`
- **Example**: `NOTE "Hello, World!"`


## Closing Remarks

This project is **open-source** and is still in the **testing phase**. We welcome contributions, bug reports, and feature requests from the community. As the project is in development, some features may be subject to change, and there may be bugs that need to be addressed.

Feel free to fork the repository, submit pull requests, or open issues to help improve this assembler.

### License
This project is licensed under the [MIT License](LICENSE).

Thank you for your interest in this project, and we appreciate any support you can provide during its development!
