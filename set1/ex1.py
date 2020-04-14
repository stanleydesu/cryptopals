import base64
def hexToBase64(hex_string):
	return base64.b64encode(bytes.fromhex(hex_string)).decode('utf-8')

assert hexToBase64("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d") == "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"