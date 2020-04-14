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

lines = open('ex4.txt').read().splitlines()
xor_texts = []
for hexstring in lines:
    encoded_bytes = bytes.fromhex(hexstring)
    xor_texts.append(bruteforce_single_xor(encoded_bytes))
top_score = sorted(xor_texts, key=lambda x: x['score'], reverse=True)[0]
for key in top_score:
    print(f"{key}: {top_score[key]}")