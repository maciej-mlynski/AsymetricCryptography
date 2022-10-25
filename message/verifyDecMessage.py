from Crypto.Cipher import AES
from ecdsa import curveOperations as c
from entropy import randHex as rh
from hash_method import SHA_256


class ReciveMessage(c.ElipticCurveOperations):
    
    def __init__(self, enc_message, r_point, sender_pk):
        self.enc_message = enc_message
        self.r_point = r_point
        self.sender_pk = sender_pk
        
        
        c.ElipticCurveOperations.__init__(self)
    
    # User can, but do not have to verify sender, by passing his public key and compare it with point_k
    def verify_sender(self, sign, k2, point_k):
        
        Xk, s = sign
        
        w = super().inverse_mod(s, self.n)

        u1 = (k2 * w) % self.n
        u2 = (Xk * w) % self.n

        ver = super().point_add(super().point_multiply(u1, self.g),
                       super().point_multiply(u2, self.sender_pk))
    
        if ver[0] == point_k[0]:
            print('Veyfication passed')
            return 1
        else:
            print('Sender has wrong pk')
            return 0
        
    # Decryption algorythm
    @staticmethod
    def decrypt_AES_GCM(enc_message, secretKey):
        
        (ciphertext, nonce, authTag) = enc_message
        aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
        
        plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
        
        return plaintext
    
    
    def decrypt_message(self, reciver_sk):
        
        # find point s2 base on reciver sk and r_point sent by sender/different user
        s_2 = super().point_multiply(reciver_sk, self.r_point)
        
        # Now reciver use x coordinate to decrypt the message
        secret_dec_key = s_2[0]

        key = hex(secret_dec_key)[2:]
        key = bytearray.fromhex(key)

        dec_msg = self.decrypt_AES_GCM(self.enc_message, key)
        
        return dec_msg
