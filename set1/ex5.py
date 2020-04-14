def repeat_key_xor(s_bytes, key):
	keyIndex = 0
	result = b""
	encoded_bytes = str.encode("utf-8").hex()
	for b in s_bytes:
		result += bytes([key[keyIndex] ^ b])
		keyIndex = (keyIndex + 1) % len(key)
	return result

s_bytes = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = b"ICE"
print(repeat_key_xor(s_bytes, key).hex())