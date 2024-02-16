# First stage of the program
word="hello world"
word_len=len(word)
word_ascii_format=[ord(c) for c in word]
word_ascii_multi=[i*word_len for i in word_ascii_format]
word_ascii_sum=sum(word_ascii_format)
one_append= 128
message_block = [0 for i in range(64)]
print(message_block)
for i in range(word_len):
    message_block[i]=word_ascii_format[i]
message_block[word_len]=one_append
message_block[-8:] = (word_len*8).to_bytes(8, "big")

for i in range(0,len(message_block)-1,2):
    print(f"{i//2}--{message_block[i]:08b}--{message_block[i+1]:08b}")

# Second Stage of the program



