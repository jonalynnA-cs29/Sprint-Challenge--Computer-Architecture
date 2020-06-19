1- You can't pass an argument to a CALL 
so from where are you able to get the value in a CALL      
    
    If the bit string is pushed on the stack or stored in a register before issuing the CALL, it is a CALL by value

    If the address of a data structure is passed to the subroutine before the CALL instruction, it is a call by reference(address)
AKA: Where can we hold and access data in the emulator? --> Stack | Register | RAM

2- What's the result of bitwise-AND between 0b101 and 0b110?

        1 0 1
    AND 1 1 0
    -------------------
        1 0 0

    110 is binary for 6, and 101 for 5
    AND = we get 100, which is binary for 4

2- What's the result of bitwise-AND between 0b110 and 0b011?

        1 1 0
    AND 0 1 1
    -------------------
        0 1 0

    110 is binary for 6, and 011 for 3
    AND = we get 010, which is binary for 2

3 -convert 0b11001101|00101011 to hexadecimal
        11001101 : Binary (1100)(1101)
              CD : Hex     (C)   (D)
        00101011 : Binary (0010)(1011)
              2B : Hex     (2)   (B)

Hexa	0	    1	    2	    3	    4	    5	    6	    7
Binary	0000	0001	0010	0011	0100	0101	0110	0111

Hexa	8	    9	    A	    B	    C	    D	    E	    F
Binary	1000	1001	1010	1011    1100    1101    1110    1111