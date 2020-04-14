import base64
# gets the english score based off letter frequencies (sourced from Wikipedia Letter Frequencies article)
def english_score(input_bytes):
    char_freq = {
        'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .05
    }
    score = 0
    for b in input_bytes.lower():
        score += char_freq.get(chr(b), 0)
    return score

# xor all the bytes by a char
def single_xor(input_bytes, char):
    result = b""
    for b in input_bytes:
        result += bytes([b ^ char])
    return result

def bruteforce_single_xor(encoded_bytes):
    # do single_xor with all ascii values and return the top scoring xor
    xors = []
    for i in range(256):
        msg = single_xor(encoded_bytes, i)
        score = english_score(msg)
        data = {
            'message': msg,
            'score': score,
            'key': i
        }
        xors.append(data)
    return sorted(xors, key=lambda x: x['score'], reverse=True)[0]

def repeat_key_xor(s_bytes, key):
    keyIndex = 0
    result = b""
    encoded_bytes = str.encode("utf-8").hex()
    for b in s_bytes:
        result += bytes([key[keyIndex] ^ b])
        keyIndex = (keyIndex + 1) % len(key)
    return result

def hamming_distance(bytes_1, bytes_2):
    dist = 0
    for b1, b2 in zip(bytes_1, bytes_2):
        # xor so all differing bits become 1
        xor = b1 ^ b2
        for bit in bin(xor):
            if bit == "1":
                dist += 1
    return dist

def break_repeating_key(ciphertext):
    average_distances = []

    # guess keysize of 2 to 40
    for keysize in range(2, 41):
        distances = []

        chunks = [ciphertext[i: i+ keysize] for i in range(0, len(ciphertext), keysize)]
        even_chunk_len = len(chunks)
        # ensure we have an even chunk len so we always count 2 chunks at a time
        if even_chunk_len % 2:
            even_chunk_len -= 1
        for i in range(len(chunks) - 1):
            chunk1 = chunks[i]
            chunk2 = chunks[i + 1]
            distance = hamming_distance(chunk1, chunk2)
            distances.append(distance / keysize)
        result = {
            'key': keysize,
            'avg_distance': sum(distances) / len(distances)
        }
        average_distances.append(result)
    key_length = sorted(average_distances, key=lambda x: x['avg_distance'])[0]['key']
    key = b''
    for i in range(key_length):
        block = b''
        for j in range(i, len(ciphertext), key_length):
            block += bytes([ciphertext[j]])
        # get the single-byte XOR key that produces the best english score
        key += bytes([bruteforce_single_xor(block)['key']])
    return (repeat_key_xor(ciphertext, key), key) 

with open("ex6.txt") as file:
    ciphertext = base64.b64decode(file.read())
    result, key = break_repeating_key(ciphertext)
    print(f"Key: {key}\nMessage: {result}")