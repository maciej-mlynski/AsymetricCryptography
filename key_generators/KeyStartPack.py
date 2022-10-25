'''
Initialy user will generate KeyStartPack (4 values) in a specific order:
1. Entropy
2. Secret Key
3. Seed Phrase 
4. Public key

It's important for to display 1-3 points only one time. 
User must write down at least one of 2 things: secret key or seed phrase
'''


# import sys

# folder_names = ['hash_method', 'ecdsa', 'entropy']

# for folder_name in folder_names:
#     sys.path.insert(0, f'../../AsymetricCryptography/{folder_name}')

# import SHA_256
# import curveOperations as c
# import randHex as rh


from key_generators import seedPhrase as sp
from entropy import randHex as rh
from ecdsa import curveOperations as c
from hash_method import SHA_256


        
class KeyStart(c.ElipticCurveOperations, sp.SeedPhraseGenerator, rh.GenRandomHex):
    
    def __init__(self, seed_12 = True, seed_24 = False):
        self.seed_12 = seed_12
        self.seed_24 = seed_24
        c.ElipticCurveOperations.__init__(self)
        
        '''
        User can choese between 12 and 24 words seed phrase
        '''
        
    def validate_seed_selection(self):
        
        if self.seed_12 == self.seed_24:
            raise ValueError('Select exacly one seed phrase length')
        
    @staticmethod
    def secret_key(entropy):
        
        return int(SHA_256.double_sha256(entropy), 16)
    
    
    # sk -> secret key
    def public_key(self, sk, compressed=False):
        
        x, y = super().point_multiply(sk)
        
        if not compressed:
            return x, y
        
        if y % 2 == 1: # If the Y value for the Public Key is odd.
            return "03"+str(hex(x)[2:]).zfill(64)
        else: # Or else, if the Y value is even.
            return "02"+str(hex(x)[2:]).zfill(64)

    def gen_start_pack(self, with_com):
        
        # Check seed length selection
        self.validate_seed_selection()
        
        # 1. Gen entrophy
        entropy = super().gen_hex_entropy(self.seed_12, self.seed_24) # 12 words = 128 bits, 24 words = 256 bits

        # 2. Gen secret key with sha-256
        sk = self.secret_key(entropy)
        
        # 3. Gen seed phrase
        seed = super().generate_seed_phrase(entropy, hex(sk)[2:])
        
        # 4. Gen public key coordinates
        pk_coordinates = self.public_key(sk)
        
        # 4.2 public key compressed
        pk = self.public_key(sk, True)
        
        if with_com:
        
            results = f' \t\t Your sercer key: \t {hex(sk)} \n\
                Your seed phrase is: \t {seed} \n \
                Your public key is: \t {pk}'
                
            return results
        
        return sk, seed, pk_coordinates
    
        
        
    