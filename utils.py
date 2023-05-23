def write_file(path, data):
	with open(path, "wt") as chat:
		chat.writelines(line + '\n' for line in data)

def read_file(path):
	with open(path, "rt") as chat:
		data = chat.readlines()
	return data