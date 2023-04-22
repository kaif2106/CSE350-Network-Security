from tss import tsa
import hashing
from ca import CA
import my_rsa as rsa

_CA = CA(67, 79)
_TSA = tsa(61, 53)
_CA.set_tss_pu(_TSA.getPU())

class user:
    def verifyCert(self, cert):
        return ((hashing.hash_text(str(cert["Certificate"])) == rsa.decrypt(_CA.getPU(), cert["Hash"])))

    def getTSScertificate(self):
        tss_cert = _CA.get_tss_certificate()
        if self.verifyCert(tss_cert):
            return tss_cert

    def get_time_stamp(self, filename):
        file_hash = hashing.hash_file(filename)
        certificate = self.getTSScertificate()
        tsa_PU = certificate["Certificate"]
        encrypted_ts = _TSA.time_stamp(rsa.encrypt(tsa_PU, file_hash))
        return encrypted_ts
    
    def check_ts(self, filename, ts):
        file_hash = hashing.hash_file(filename)
        hash = hashing.hash_text(file_hash+ts["Timestamp"])
        ts_hash = ts["Hash"]
        decrypted_ts_hash = rsa.decrypt(self.getTSScertificate()["Certificate"], ts_hash)
        return hash==decrypted_ts_hash

A = user()
ts = A.get_time_stamp("test_file.csv")
print(ts)
print(A.check_ts("test_file.csv", ts))