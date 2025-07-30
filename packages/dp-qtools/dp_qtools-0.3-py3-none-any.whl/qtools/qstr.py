import random
import string

def generate_short_uuid() -> str:
	"""
	Return a random short UUID (6 characters)

	Example output: "q35HZa"
	"""
	charset = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
	length = 6
	return ''.join(random.choice(charset) for _ in range(length))