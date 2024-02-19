import struct

def next_multiple_512(word_len):
    l=word_len
    curr_block_size=512
    k =448%curr_block_size-l-1
    block_size=curr_block_size
    counter=1
    while True:
        if not (k <= 0):
            break
        counter += 1
        curr_block_size *= counter
        k = (curr_block_size-64) % curr_block_size - l - 1
        block_size = curr_block_size

    return block_size

def right_rotation_bit(number, rotations, int_bits=32):
    mask = 2 ** int_bits - 1
    return ((number & mask) >> rotations) | ((number & mask) << (int_bits - rotations)) & mask


def right_shift(number, shift, int_bits=32):
    mask = 2 ** int_bits - 1
    return ((number & mask) >> shift) & mask


def sigma_zero(number):
    mask = 2 ** 32 - 1
    return (right_rotation_bit(number, 7) ^ right_rotation_bit(number, 18) ^ right_shift(number, 3)) & mask


def sigma_one(number):
    mask= 2 ** 32 -1
    return (right_rotation_bit(number, 17) ^ right_rotation_bit(number, 19) ^ right_shift(number, 10)) & mask


def message_proc(message_id, message_chunk):
    mask = 2 ** 32 - 1
    w_t = (sigma_one(message_chunk[message_id-2]) + message_chunk[message_id-7] + sigma_zero(message_chunk[message_id-15]) + message_chunk[message_id-16]) & mask
    return w_t

def majority_proc(a, b, c):
    mask = 2 ** 32 - 1
    return ((a & b) ^ (a & c) ^ (b & c)) & mask

def choose_proc(e, f, g):
    mask = 2 ** 32 - 1
    return ((e & f) ^ ((~e) & g)) & mask

def sum_zero(a):
    mask = 2 ** 32 - 1
    return (right_rotation_bit(a, 2) ^ right_rotation_bit(a, 13) ^ right_rotation_bit(a, 22)) & mask

def sum_one(e):
    mask = 2 ** 32 - 1
    return (right_rotation_bit(e, 6) ^ right_rotation_bit(e, 11) ^ right_rotation_bit(e, 25)) & mask


def temp1_proc(e_x, f_x, g_x, h_x, msg_idx, message_chunk):
    mask = 2 ** 32 - 1
    return (h_x + sum_one(e_x) + choose_proc(e_x, f_x, g_x) + k_constants[msg_idx] + message_chunk[msg_idx]) & mask


def temp2_proc(a, b, c):
    mask = 2 ** 32 - 1
    return (sum_zero(a) + majority_proc(a, b, c)) & mask


# First stage of the program
word="CitricSheep"
mask=2 ** 32 -1
word_len=len(word)
word_ascii_format=[ord(c) for c in word]
word_ascii_multi=[i*word_len for i in word_ascii_format]
word_ascii_sum=sum(word_ascii_format)
one_append= 128
block_size_bytes=int(next_multiple_512(word_len) / 8)
message_block = [0 for i in range(block_size_bytes)]


print(message_block)
for i in range(word_len):
    message_block[i]=word_ascii_format[i]
message_block[word_len]=one_append
message_block[-8:] = (word_len*8).to_bytes(8, "big")

for i in range(0,len(message_block)-1,2):
    print(f"{i//2}--{message_block[i]:08b}--{message_block[i+1]:08b}")

# Second Stage of the Program
# 64 blocks of 32bit words (4*8*64)
message_chunk=[0 for i in range(64)]

counter = 0
for i in range(0,len(message_block),4):
    message_chunk[counter]= struct.unpack(">I",bytes(message_block[i: i + 4]))[0]
    counter += 1
print("\n")
for i in range(len(message_chunk)):
    print(f"w{i}--{message_chunk[i]:032b}")

#SHA-256 HASH Computation
for msg_idx in range(len(message_chunk)):
    if msg_idx >= 16 and msg_idx <= 63:
        message_chunk[msg_idx] = message_proc(msg_idx, message_chunk)


for i in range(len(message_chunk)):
    print(f"w{i}--{message_chunk[i]:032b}")


#Second Stage
#hash values h0 to h7, first 32 bits of the fractional parts of the square roots of the first
# 8 primes 2..9
h0=0x6a09e667
h1=0xbb67ae85
h2=0x3c6ef372
h3=0xa54ff53a
h4=0x510e527f
h5=0x9b05688c
h6=0x1f83d9ab
h7=0x5be0cd19

k_constants = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
               0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
               0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
               0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
               0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
               0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
               0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
               0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]
a = h0
b = h1
c = h2
d = h3
e = h4
f = h5
g = h6
h = h7

for msg_idx in range(len(message_chunk)):
    t1 = temp1_proc(e, f, g, h, msg_idx, message_chunk)
    t2 = temp2_proc(a, b, c)
    h = g
    g = f
    f = e
    e = (d + t1) & mask
    d = c
    c = b
    b = a
    a = (t1 + t2) & mask

h0 = (a + h0) & mask
h1 = (b + h1) & mask
h2 = (c + h2) & mask
h3 = (d + h3) & mask
h4 = (e + h4) & mask
h5 = (f + h5) & mask
h6 = (g + h6) & mask
h7 = (h + h7) & mask


print(hex(h0))
print(hex(h1))
print(hex(h2))
print(hex(h3))
print(hex(h4))
print(hex(h5))
print(hex(h6))
print(hex(h7))


print(struct.pack(">8I", h0, h1, h2, h3, h4, h5, h6, h7).hex())