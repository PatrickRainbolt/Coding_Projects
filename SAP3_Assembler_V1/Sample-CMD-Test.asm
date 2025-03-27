; Test Script for SAP-3, Simple AS Posible Version 3, Assembly Instructions

            ; Testing NOP (No operation)
			NOP                 ; No operation (do nothing)

            ; Testing LDA (Load from memory)
			LDI     R0, 5       ; Load immediate value 5 into R0
			MOV     R0, A       ; Loads R0 into the Accumulator
			STA     0x00        ; Store value of Accumulator into memory address 0x00
			LDA     0x00        ; Load value from memory address 0x00 into accumulator
			NOTE    "Testing LDA:  R0[{R0}] A[{A}] 0x00[{0x00}]  Answer should be 5"
			OUT                 ; Output the value in the accumulator

            ; Testing STA (Store to memory)
			LDI     R1, 10      ; Load immediate value 10 into R1
			MOV     R1, A       ; Loads R1 into the Accumulator
			STA     0x01        ; Store value of Accumulator into memory address 0x01
			LDA     0x01        ; Load value from memory address 0x01 into accumulator
			NOTE    "Testing STA: R1[{R1}] A[{A}] 0x01[{0x01}]  Answer should be 10"
			OUT                 ; Output the value in the accumulator

            ; Testing ADD (Add register value to accumulator)
			LDI     R0, 3       ; Load immediate value 3 into R0
			MOV     R0, A       ; Loads R0 into the Accumulator
			STA     0x02        ; Store value of Accumulator into memory address 0x02
			LDA     0x00        ; Load value from memory address 0x00 into accumulator
			ADD     0x02        ; Add value from memory address 0x02 to accumulator (5 + 3 = 8)
			NOTE    "Testing ADD: R0[{R0}] A[{A}] 0x02[{0x02}]  Answer should be 8"
			OUT                 ; Output the value in the accumulator

            ; Testing SUB (Subtract value from memory)
			LDI     R2, 7       ; Load immediate value 7 into R2
			MOV     R2, A       ; Loads R2 into the Accumulator
			STA     0x03        ; Store value of Accumulator into memory address 0x03
			LDA     0x00        ; Load value from memory address 0x00 into accumulator
			SUB     0x03        ; Subtract value from memory address 0x03 from accumulator (5 - 7 = -2)
			NOTE    "Testing SUB: R0[{R0}] A[{A}] 0x03[{0x03}]  Answer should be -2"
			OUT                 ; Output the value in the accumulator

            ; Testing AND (Logical AND with accumulator)
			LDI     R3, 3       ; Load immediate value 3 into R3
			MOV     R3, A       ; Loads R3 into the Accumulator
			STA     0x04        ; Store value of R3 into memory address 0x04
			LDA     0x00        ; Load value from memory address 0x00 into accumulator
			AND     0x04        ; Perform AND with value from memory address 0x04
			NOTE    "Testing ADD: R3[{R3}] A[{A}] 0x04[{0x04}]  Answer should be 1"
			OUT                 ; Output the value in the accumulator

            ; Testing OR (Logical OR with accumulator)
			LDI     R4, 2       ; Load immediate value 2 into R4
			MOV     R4, A       ; Loads R4 into the Accumulator
			STA     0x05        ; Store value of R4 into memory address 0x05
			LDA     0x00        ; Load value from memory address 0x00 into accumulator
			OR      0x05        ; Perform OR with value from memory address 0x05
			NOTE    "Testing OR: R4[{R4}] A[{A}] 0x05[{0x05}]  Answer should be 7"
			OUT                 ; Output the value in the accumulator

            ; Testing XOR (Logical XOR with accumulator)
			LDI     R5, 5       ; Load immediate value 5 into R5
			MOV     R5, A       ; Loads R5 into the Accumulator
			STA     0x06        ; Store value of Accumulator into memory address 0x06
			LDA     0x00        ; Load value from memory address 0x00 into accumulator
			XOR     0x06        ; Perform XOR with value from memory address 0x06
			NOTE    "Testing XOR: R5[{R5}] A[{A}] 0x00[{0x00}] 0x06[{0x06}]  Answer should be 0"	
			OUT                 ; Output the value in the accumulator

            ; Testing JMP (Jump to label)
			JMP     TEST_JMP    ; Jump to TEST_JMP
			NOP                 ; No operation (do nothing)
			NOTE "JMP-ERROR: Didn't NotJump!"
TEST_JMP:   			        ; This label will be jumped to in the program
			LDI     R6, 42      ; Load immediate value 42 into R6
			MOV     R6, A       ; Loads R6 into the Accumulator
			NOTE    "Testing JMP: R6[{R6}] A[{A}]  Answer should be 42"
			OUT                 ; Output the value in the accumulator

            ; Testing JG (Jump if greater than zero)
			LDI     R7, 10      ; Load immediate value 10 into R7
			LDA     0x00        ; Load value from memory address 0x00 into accumulator
			JG      JUMP_JG     ; Jump if accumulator is greater than zero
			NOP                 ; No operation (do nothing)
			NOTE "JG-ERROR: Didn't NotJump!"
JUMP_JG:
			LDI		R8, 99      ; Load immediate value 99 into R8
			NOTE    "Testing JG: R7[{R7}] R8[{R8}] A[{A}] 0x00[{0x00}]  Answer should be 5"
			OUT                 ; Output the value in the accumulator

            ; Testing JZ (Jump if zero flag is set)
			LDI     R0, 0       ; Load immediate value 0 into R0
			LDA     0x00        ; Load value from memory address 0x00 into accumulator
			SUB     0x00        ; Subtract value from memory address 0x00 (5 - 5 = 0)
			JZ      JUMP_JZ     ; Jump if the result is zero
			NOP                 ; No operation (do nothing)
			NOTE "JZ-ERROR: Didn't NotJump!"
JUMP_JZ:
			LDI     R10, 1      ; Load immediate value 1 into R10
			NOTE    "Testing JZ: R0[{R0}] R10[{R10}] A[{A}] 0x00[{0x00}]  Answer should be 0"
			OUT                 ; Output the value in the accumulator

            ; Testing JC (Jump if carry flag is set)
			LDI     R11, 255    ; Load immediate value 255 into R11
			MOV     R11, A      ; Loads R11 into the Accumulator
			STA     0x07        ; Store value of R11 into memory address 0x07
			LDA     0x00        ; Load value from memory address 0x00 into accumulator
			ADD     0x07        ; Add value from memory address 0x07 to accumulator (5 + 255 = 260)
			JC      JUMP_JC     ; Jump if carry flag is set
			NOP                 ; No operation (do nothing)
			NOTE "JC-ERROR: Didn't NotJump!"
JUMP_JC:
			LDI     R12, 77     ; Load immediate value 77 into R12
			NOTE    "Testing JC: R11[{R11}] R12[{R12}] A[{A}] 0x00[{0x00}] 0x07[{0x07}]  Answer should be 0"
			OUT                 ; Output the value in the accumulator

            ; Additional Tests for Registers and Stack (PUSH, POP, MOV, etc.)
			LDI     R13, 50     ; Load immediate value 50 into R13
			MOV     R13, R14    ; Move value from R13 to R14
			MOV     R14, A      ; Loads R14 into the Accumulator
			NOTE    "Testing Reg: R13[{R13}] R14[{R14}] A[{A}]  Answer should be 50"
			OUT                 ; Output the value in the accumulator

			; PUSH - Push value from R13 to stack
			PUSH    R13         ; Push value of R13 to stack
			LDI     R15, 100    ; Load immediate value 100 into R15
			MOV     R15, A      ; Loads R15 into the Accumulator
			NOTE    "Testing Push: R13[{R13}] R15[{R15}] A[{A}]  Answer should be 100"
			OUT                 ; Output the value in the accumulator
			
			; POP - Pop value from stack to R13
			LDI     R13, 0      ; Load immediate value 0 into R13
			POP     R13         ; Pop value from stack to R13 (should be 50)
			NOTE    "Testing Pop: R13[{R13}]   Answer should be 50"
			OUT                 ; Output the value in the accumulator

			; LDR - Load value from memory location 0x08 into R14
			LDI     R15, 25     ; Load immediate value 25 into R15
			STR     R15, 0x00   ; Store value of R15 into memory address 0x00
			LDR     R14, 0x00   ; Load value from memory address 0x00 into R14
			LDA     0x00        ; Loads R14 into the Accumulator
			NOTE    "Testing LDR: R14[{R14}] R15[{R15}]   Answer should be 25"
			OUT                 ; Output the value in the accumulator

			; STR - Store value from R15 into memory location 0x07
			LDI     R15, 30     ; Load immediate value 30 into R15
			STR     R15, 0x07   ; Store value of R15 into memory address 0x07
			LDR     R14, 0x07   ; Load value from memory address 0x07 into R14
			MOV     R14, A      ; Loads R14 into the Accumulator
			NOTE    "Testing Push: R14[{R14}] R15[{R15}] A[{A}]  Answer should be 50"
			OUT                 ; Output the value in the accumulator

			; LDRI - Load immediate value 12 into R15
			LDRI    R15, 12     ; Load immediate value 12 into R15
			MOV     R15, A      ; Loads R14 into the Accumulator
			NOTE    "Testing LDRI: R15[{R15}] A[{A}]  Answer should be 12"
			OUT                 ; Output the value in the accumulator

			; LDI - Load immediate value 42 into accumulator
			LDI     R0, 42      ; Load immediate value 42 into the accumulator
			MOV     R0, A       ; Loads R0 into the Accumulator
			NOTE    "Testing LDRI: R0[{R0}] A[{A}]  Answer should be 42"
			OUT                 ; Output the value in the accumulator

			; Testing HLT (Halt the program)
			HLT                 ; Halt the program execution

