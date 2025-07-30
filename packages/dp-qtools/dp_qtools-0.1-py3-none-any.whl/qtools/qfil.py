import os

def get_lines_from_file(file_name: str) -> list[str]:
	"""
	Get all lines from a file as a list of strings.

	Usage:
		lines = get_lines_from_file("../../notes.txt")
	"""
	try:
		with open(file_name, "r", encoding="utf-8") as f:
			contents = f.read()
	except Exception as e:
		raise RuntimeError(f"Failed to read file: {e}")

	lines = [line.strip() for line in contents.split('\n')]
	return lines
