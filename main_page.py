'''
STEP #1
1.1 Gen random entropy
1.2 Gen seed phrase
1.3 Gen secret key
1.4 Gen public key
---All should be done symtricly for sender and reciver---

STEP #2
2.1 Write and encrypt message
2.2 Sign message
2.3 Recive enc message -> verify
2.4 Decrypt message

STEP #3
3.1 Remaind secret key by seed phrase
3.2 Remind public key by secret or pk
'''

from key_generators import KeyStartPack
from message import signEncMessage, verifyDecMessage




# First user -> 256 lenght entropy -> 128=False, 256=True
user1 = KeyStartPack.KeyStart(False, True)

# Print keys in compressed form
print('Sender values:')
print(user1.gen_start_pack(True))

# Save keys as variables
sk1, seed1, pk1 = user1.gen_start_pack(False)


# Second user -> 128 lenghts entropy
user2 = KeyStartPack.KeyStart(True, False)

# Print keys in compressed form
print('------------------------------')
print('Receiver values:')
print(user2.gen_start_pack(True))

# Save keys as variables
sk2, seed2, pk2 = user2.gen_start_pack(False)

# User1 -> sender
# User2 -> recipient

message1 = b"Hello everyone! Creating a tool for encrypting messages was a pure pleasure for me. I learned a lot of interesting things that I'm sure will be useful in the future. Now it's time for the big security test of my code. If I haven't made a mistake anywhere, no one should be able to read this message."

# initialize/specify the recipient
mesageencryption = signEncMessage.SendMessage(pk2)

# sign message
sign, k2, point_k = mesageencryption.sign_transaction(sk1)
print('------------------------------')
print('Verification values')
print(f'Signature: {sign}')
print(f'K2: {k2}')
print(f'K Pooint: {point_k}')

# this values can be seen by third participians.
# Anyone can prove that user1 send this message, base on his public key 

# gen encrypt message with r_point -> both can be seen by trhird participians
r_point, enc_message = mesageencryption.gen_encrypt_message(message1)
print('------------------------------')
print('Message values')
print(f'R Point: {r_point}')
print(f'Enc Message: {enc_message}')


# Base on r_point user2 can encript message, but before 
# initialize
messageVerDec = verifyDecMessage.ReciveMessage(enc_message, r_point, pk1)

# lets's verify sender
messageVerDec.verify_sender(sign, k2, point_k)

# decrypt message
a = messageVerDec.decrypt_message(sk2)
print(a)

