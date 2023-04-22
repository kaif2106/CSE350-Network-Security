import hashlib

def hash_text(input_text): #Hashing function - SHA256
    input_text = input_text.encode()
    sha = hashlib.sha256()
    sha.update(input_text)
    hex_hash = sha.hexdigest()
    hex_hash = str(hex_hash)
    return hex_hash

def hash_file(file):
	# 65536 = 65536 bytes = 64 kilobytes
	BUF_SIZE = 65536
	sha256 = hashlib.sha256()
	with open(file, 'rb') as f:	
		while True:
			data = f.read(BUF_SIZE)
			if not data:
				break
			sha256.update(data)
	return sha256.hexdigest()
