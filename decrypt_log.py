import sys

def parity_bit(n):
    parity = 0
    while (n != 0):
        if ((n & 1) == 1):
            parity = parity ^ 1
        n = n >> 1
    return parity

in_file = open(sys.argv[1], "rb")
in_bytes = in_file.read()
in_file.close()

num_bytes = len(in_bytes)
scramble_key = 0xff

out_bytes = bytearray(num_bytes)

for i in range(0,num_bytes):
    scramble_key = (scramble_key >> 1) | (parity_bit(scramble_key & 0xc3) << 7)
    adjust_index = num_bytes - 1 - i
    out_bytes[adjust_index] = in_bytes[adjust_index] ^ scramble_key

out_file = open(sys.argv[1] + ".txt", "wb")
out_file.write(out_bytes)
out_file.close()
