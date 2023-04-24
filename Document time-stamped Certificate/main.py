from tss import tsa
import hashing
from ca import CA
import my_rsa as rsa
import json

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
while True:
    ch = int(input(("1. Timestamp document\n2. Verify document with timestamp\n3. Exit\n")))
    if ch==1:
        filename = input("Filename: ")
        ts = A.get_time_stamp(filename)
        saveas = input("Save timestamp as: ")
        with open(f'{saveas}.json', 'w') as f:
            json.dump(ts, f)
    elif ch==2:
        filename = input("Filename: ")
        ts_filename = input("Timestamp file name: ")
        with open(f'{ts_filename}.json', 'r') as f:
            ts = json.load(f)
        print(A.check_ts(filename, ts))
    else: break