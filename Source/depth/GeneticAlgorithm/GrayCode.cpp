#include "GrayCode.h"

uint BinaryToGray(uint num)
{
    return num ^ (num >> 1);
}

uint GrayToBinary(uint num)
{
    uint mask = num;
    while (mask) 
    {
        mask >>= 1;
        num ^= mask;
    }
    return num;
}

uint GrayToBinary32(uint num)
{
    num ^= num >> 16;
    num ^= num >> 8;
    num ^= num >> 4;
    num ^= num >> 2;
    num ^= num >> 1;
    return num;
}

uint get_bit(uint n, uint k)
{
    return (n & (1 << k)) >> k;
}

void set_bit(uint& n, uint k, uint v)
{
    n = (n & ~(1UL << k)) | (v << k);
}