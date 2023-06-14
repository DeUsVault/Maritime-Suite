#pragma once
typedef unsigned int uint;

// This function converts an unsigned binary number to reflected binary Gray code.
uint BinaryToGray(uint num);

// This function converts a reflected binary Gray code number to a binary number.
uint GrayToBinary(uint num);

// A more efficient version for Gray codes 32 bits or fewer through the use of SWAR (SIMD within a register) techniques. 
// It implements a parallel prefix XOR function. The assignment statements can be in any order.
// 
// This function can be adapted for longer Gray codes by adding steps.
uint GrayToBinary32(uint num);

uint get_bit(uint n, uint k);

void set_bit(uint& n, uint k, uint v);