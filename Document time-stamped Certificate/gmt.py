import requests
import hashing
import my_rsa as rsa

class gmt_server:
    def __init__(self, p, q):
        self._url_hash = hashing.hash_text("https://worldtimeapi.org/api/timezone/Etc/GMT")
        self.p = p
        self.q = q
        self.public_key, self.private_key = rsa.generate_keypair(p,q)

    def getPU(self):
        return self.public_key

    def get_gmt(self):
        url = "https://worldtimeapi.org/api/timezone/Etc/GMT"
        # Set the API endpoint URL
        if hashing.hash_text(url)!=self._url_hash:
            return "Error"

        # Send a GET request to the API endpoint
        response = requests.get(url)

        # Check if the response status code is OK (200)
        if response.status_code == 200:
            # Parse the JSON response to obtain the current GMT time
            data = response.json()
            current_time = data['datetime']
            return rsa.encrypt(self.private_key, current_time)
        else:
            # Handle the error case
            print("Error:", response.status_code)
            return "Error"