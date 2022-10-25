'''
COMMENT
i
'''

import random
from randomgen import Xoroshiro128
from numpy.random import Generator



class GenRandomHex:
    
    @staticmethod
    def gen_random_shuffle():
        
        # rg will generate decimal number 
        rg = Generator(Xoroshiro128(random.randint(1, 2**56), plusplus=True))
        
        # multiply number by random number, than take absolute value and make it int
        return int(abs(rg.standard_normal() * random.randint(1, 2**56)))
    
    
    @staticmethod
    def repair_entropy_length(entropy, prop_length):
    
        while len(entropy) != prop_length:
            
            # choese random number in range of entropy length
            n = random.randint(1, len(entropy))
            # choese random hex character
            character = hex(random.getrandbits(4))[2:]
            # place random hex character in random place
            entropy = entropy[:n] + f'{character}' + entropy[n:]
            
            
        return entropy
            
            
    def gen_hex_entropy(self, bit_128=False, bit_256 = True):
    
        if bit_128 == 0 and bit_256 == 0:
            print('Select at least one bit length')
            return 0
        
        if bit_128 and bit_256:
            print('You can select only one bit length')
            return 0
        
        # properties for 256 bits length
        bits = 256
        length = 64
        
        # properties for 128 bits length
        if bit_128:
            bits = 128
            length = 32
        
        entropy = hex(random.getrandbits(bits))[2:]
        
        # Sometimes generator create hex with wrong length
        # eg. 128 bit entropy should gen hex with 32 length, but instead it generate hex with length 31
        # so instead of runing function again -> add one or more characters in random place to str entropy
        entropy = self.repair_entropy_length(entropy, length)
        
        # To double protect entropy 
        # gen random number by Xoroshiro128 algorytm
        shufle_rep = self.gen_random_shuffle()
        
        # random number will shufle our entropy
        while shufle_rep:
            
            # shufling will be done only when the bit of out shufle_rep == 1
            if shufle_rep & 1:
                # shufle method
                entropy = ''.join(random.sample(entropy,len(entropy)))
            
            # cut last bit of shufle_rep number
            shufle_rep >>= 1
            
        return entropy
    
    
# gen = GenRandomHex()

# for i in range(10000):
#     entropy = gen.gen_hex_entropy()
#     print(entropy)

