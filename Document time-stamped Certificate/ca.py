import my_rsa as rsa
import hashing

class CA:
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.public_key, self.private_key = rsa.generate_keypair(p,q)
    
    def set_tss_pu(self, pu):
        self.tss_PU = pu

    def getPU(self):
        return self.public_key
    
    def get_tss_certificate(self):
        certificate_hash = rsa.encrypt(self.private_key, hashing.hash_text(str(self.tss_PU)))
        certificate = {"Certificate":self.tss_PU, "Hash":certificate_hash}
        return certificate
