from Crypto.Cipher import AES
from ecdsa import curveOperations as c
from entropy import randHex as rh
from hash_method import SHA_256



class SendMessage(c.ElipticCurveOperations, rh.GenRandomHex):
    
    def __init__(self, recipient_pk):
        self.recipient_pk = recipient_pk   
             
        c.ElipticCurveOperations.__init__(self)
    
    
    def create_random_k_number(self):
        
        # random entropy
        entropy = super().gen_hex_entropy(bit_128=False, bit_256 = True)
        
        return int(SHA_256.double_sha256(entropy), 16)
    
    # Sign transaction with private key in case user want to verify sender
    def sign_transaction(self, sender_sk):
        
        # First level of security: Gen random number
        k = self.create_random_k_number()
        
        # Place vlue on the Eliptic Curve
        point_k = super().point_multiply(k, self.g)
        
        # Coordinates of point
        Xk, Yk = point_k
        
        # Second level of security: Gen random hex
        k2 = self.create_random_k_number()
        
        # Calculate S value
        s = (super().inverse_mod(k, self.n) * (k2 + sender_sk * Xk)) % self.n
        
        sign = [Xk, s]
        
        return sign, k2, point_k
    
    # Message encryption algorytm
    @staticmethod
    def encrypt_AES_GCM(msg, secretValue):
        
        aesCipher = AES.new(secretValue, AES.MODE_GCM)
        ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
        
        return (ciphertext, aesCipher.nonce, authTag)
    
    def gen_encrypt_message(self, message):
        
        # 1. Generate random 256 bit number hashed with SHA-256 (double)
        # WAR!: Different from previous k and nonce (number used once)
        k = self.create_random_k_number()
    
        # 2. Calc radom point on curver -> will be sent too reciver
        r_point = super().point_multiply(k)
        
        # 3. Calculate secret key to encrypt message (use random number + reciver public key)
        secret_values = super().point_multiply(k, self.recipient_pk)
        
        encryption_key = secret_values[0]
        
        enc = hex(encryption_key)[2:]
        enc_bytes = bytearray.fromhex(enc)
        
        # Use our method to encrypt message with sercet signature 
        enc_message = self.encrypt_AES_GCM(message, enc_bytes)

        return r_point, enc_message
    
    
