## RSA Certification

![image](https://user-images.githubusercontent.com/29958259/228498242-f6b52a34-5e41-49a8-8070-c3c2555bfa38.png)

### Scheme
![image](https://user-images.githubusercontent.com/29958259/228499533-760764b5-4fdc-42bc-b136-2f594433bbc5.png)


CERTA = ENCPR-CA (IDA, PUA, TA, DURA, IDCA),
where (you decide the format for each of these):
• PR-CA is private key of certification authority (PU-CA is public key of certification authority)
• IDA is user ID of A, IDCA is the ID of the CA,
• PUA is public key of A,
• TA is time of issuance of certificate, and DURA is the duration for which the certificate is valid.

### Assumptions
1. That clients already (somehow) know their own [private-key, public-key], but do not have their own
certificates or that of others,
2. That clients already (somehow) know the public key of the certification authority,
3. That CA has the public keys of all the clients.

### Tasks
- Decide that messages from CA to clients are encrypted using RSA algorithm and CA’s private key,
- Encrypted messages are sent/received between clients once they have each other client’s public key, and
- Find a way to generate and encode “current time”, and “duration”.
- Think hard as to who generates the pair of keys, viz. [private-key, public-key], and how do the
CA and/or client get to know it.

### Test
As a test, use the above to determine each other’s public key, and then ensure client A can send 3 messages to B, viz.
Hello1, Hello2, and Hello3. Client B in turn responds with ACK1, ACK2, and ACK3 to messages received from A.
