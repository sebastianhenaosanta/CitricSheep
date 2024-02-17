import struct

def right_rotation_bit(number, rotations, int_bits=32):
    mask = 2 ** int_bits - 1
    return ((number & mask) >> rotations) | ((number & mask) << (int_bits - rotations)) & mask

def right_shift(number, shift, int_bits=32):
    mask = 2 ** int_bits - 1
    return ((number & mask) >> shift) & mask

def sigma_zero(number):
    return right_rotation_bit(number, 7) ^ right_rotation_bit(number, 18) ^ right_shift(number, 3)

def sigma_one(number):
    return right_rotation_bit(number, 17) ^ right_rotation_bit(number, 19) ^ right_shift(number, 10)


# First stage of the program
word="hello world"
word_len=len(word)
word_ascii_format=[ord(c) for c in word]
word_ascii_multi=[i*word_len for i in word_ascii_format]
word_ascii_sum=sum(word_ascii_format)
one_append= 128
message_block = [0 for i in range(64)]

#Setting Initial Hash Value
h_0=0x6a09e667
h_1=0xbb67ae85
h_2=0x3c6ef372
h_3=0xa54ff53a
h_4=0x510e527f
h_5=0x9b05688c
h_6=0x1f83d9ab
h_7=0x5be0cd19

print(message_block)
for i in range(word_len):
    message_block[i]=word_ascii_format[i]
message_block[word_len]=one_append
message_block[-8:] = (word_len*8).to_bytes(8, "big")

for i in range(0,len(message_block)-1,2):
    print(f"{i//2}--{message_block[i]:08b}--{message_block[i+1]:08b}")

# Second Stage of the Program
# 64 blocks of 32bit words (4*8*64)
message_chunk=[[0 for i in range(4)] for j in range(64)]

slider = 0
counter = 0
while slider < len(message_block):
    message_chunk[counter] = struct.unpack(">I",bytes(message_block[slider: slider + 4]))[0]
    slider += 4
    counter += 1


# for i in range(len(message_chunk)):
#     row_byte_arr = bytes(message_chunk[i])
#     unpacked_number = struct.unpack(">I", row_byte_arr)[0]
#     print(f"w{i}--{unpacked_number:032b}")

