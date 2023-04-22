from gmt import gmt_server
import hashing
import my_rsa as rsa

class tsa:
    def __init__(self, p, q):
        self.my_gmt_server = gmt_server(83, 97)
        self.p = p
        self.q = q
        self.public_key, self.private_key = rsa.generate_keypair(p,q)

    def getPU(self):
        return self.public_key

    def time_stamp(self, ehash):
        hash = rsa.decrypt(self.private_key, ehash)
        time = rsa.decrypt(self.my_gmt_server.getPU(), self.my_gmt_server.get_gmt())
        message = hash+time
        hashed_message = hashing.hash_text(message)
        encrypted = rsa.encrypt(self.private_key, hashed_message)
        return {"Hash": encrypted, "Timestamp":time}