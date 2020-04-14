def hexToInt(hex_string):
	return int(hex_string, 16)

def fixed_xor(s1, s2):
	# convert both strings to ints
	b1 = hexToInt(s1)
	b2 = hexToInt(s2)
	# cut off the 0x prefix and return it
	return hex(b1 ^ b2)[2:] 

assert fixed_xor("1c0111001f010100061a024b53535009181c", "686974207468652062756c6c277320657965") == "746865206b696420646f6e277420706c6179"