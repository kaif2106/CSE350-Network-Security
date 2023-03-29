# create clients and CA
# A requests CA for B's certificate
# A verifies the certificate
# A sends B a message using PUb obtained from verified certificate
# B decrypts message using PRb
# B requests CA for A's certificate
# B verifies the certificate
# B sends A a message using PUa obtained from verified certificate
# A decrypts message using PRa

import my_rsa as rsa
import time
import hashlib


def sha256(input_text): #Hashing function - SHA256
    input_text = input_text.encode()
    sha = hashlib.sha256()
    sha.update(input_text)
    hex_hash = sha.hexdigest()
    hex_hash = str(hex_hash)
    return hex_hash

class CA:
    def __init__(self, ID, p, q):
        self.ID = ID
        self.p = p
        self.q = q
        self.PUs = {}
        self.public_key, self.private_key = rsa.generate_keypair(p,q)
    
    def set_PUs(self, ID, PU):
        self.PUs[ID] = PU

    def get_certificate(self, request):
        decrypted_request = rsa.decrypt(self.private_key, request)
        i = int(decrypted_request)
        info = {"ID":i, "CA ID":self.ID, "PU":self.PUs[i], "T":int(time.time()), "DUR":60}
        certificate = rsa.encrypt(self.private_key, sha256(str(info)))
        return {"Certificate":info, "Hash":certificate}

class client:
    def __init__(self, ID, p, q, CA_PU):
        self.ID = ID 
        self.p = p
        self.q = q
        self.CA_PU = CA_PU
        self.certificates = {}
        self.public_key, self.private_key =  rsa.generate_keypair(p,q)
    
    def get_request(self, IDx):
        return rsa.encrypt(self.CA_PU, str(IDx))
    
    def add_cert(self, ID, cert):
        self.certificates[ID] = cert
    
    def check_cert(self, ID):
        if ID in self.certificates.keys():
            return True
        return False

    def get_cert(self, ID):
        return self.certificates[ID]
    
    def verify_cert(self, cert):
        return ((sha256(str(cert["Certificate"])) == rsa.decrypt(self.CA_PU, cert["Hash"])) and (cert["Certificate"]["T"]+cert["Certificate"]["DUR"]>time.time()))
    
    def show_certificates(self):
        print(self.certificates)


C = CA(3, 67, 79)
clients = {}
clients[1] = client(1, 61, 53, C.public_key)
clients[2] = client(2, 83, 97, C.public_key)
C.set_PUs(1, clients[1].public_key)
C.set_PUs(2, clients[2].public_key)

while True:
    c = int(input("1. Create new client\n2. Client Login\nEnter: "))
    i = int(input("ID: "))
    if c==1:
        p = int(input("p: "))
        q = int(input("q: "))
        clients[i] = client(i, p, q, C.public_key)
        C.set_PUs(i, clients[i].public_key)
    else:
        c2 = 1
        while c2!=5:
            c2 = int(input("1. Request CA for certificate\n2. Check available certificates\n3. Send message\n4. Check messages\n5. Logout\nEnter: "))
            if c2==1:
                r = int(input("Enter ID of client: "))
                request = clients[i].get_request(r)
                cert = C.get_certificate(request)
                print("Certificate of client "+str(r)+" recieved")
                if clients[i].verify_cert(cert):
                    print("Certificate of client "+str(r)+" verified")
                    clients[i].add_cert(r, cert)
                else:
                    print("Certificate of client "+str(r)+" is incorrect")
            if c2==2:
                clients[i].show_certificates()
            if c2==3:
                r = int(input("Enter ID of client: "))
                if clients[i].check_cert(r):
                    if clients[i].verify_cert(clients[i].get_cert(r)):
                        message = input("Enter message: ")
                    else: print("Certificate is incorrect or has expired. Please create a new certificate")
                else: print("Certificate does not exist")
            
                



A = client(1, 61, 53, C.public_key)
B = client(2, 83, 97, C.public_key)
PUs = {A.ID:A.public_key, B.ID:B.public_key}
C.set_PUs(PUs)
request = A.get_request(2)
cert = C.get_certificate(request)
if A.verify_cert(cert):
    print("Y")
else: print("N")


#cer = C.get_certificate(A)
#print(sha256(str(cer["Certificate"])) == rsa.decrypt(C.private_key, cer["Hash"]))




