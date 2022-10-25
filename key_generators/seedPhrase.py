import pandas as pd
import numpy as np

bip39 = pd.read_csv('../AsymetricCryptography/BIP-39/bip39')

class SeedPhraseGenerator:
    
    @staticmethod
    def check_bin_lenght(entropy):
        
        bin_entropy = bin(int(entropy, base=16))[2:]
        
        if len(bin_entropy) <= 128:
            prop_length = 128
            check_sum_length = 1
            
            return prop_length, check_sum_length
        
        prop_length = 256
        check_sum_length = 2
        
        return prop_length, check_sum_length
        
    
    def entropy_to_binary(self, entropy):
        
        bin_entropy = bin(int(entropy, base=16))[2:]
        prop_length= self.check_bin_lenght(entropy)[0]
        
        # Check len of bin entropy
        if len(bin_entropy) == prop_length:
            pass
        else:
            # if len < 128 it means that we must add extra 0 in the begining of the bin_entropy string
            bin_entropy = (prop_length - len(bin_entropy)) * '0' + bin_entropy

        return bin_entropy
    
    def check_sum(self, entropy, sk):
        
        check_sum_length = self.check_bin_lenght(entropy)[1] # 1 for 128 bit entropy, 2 for 256 entropy
        check_sum_character = sk[:check_sum_length]
        check_sum_bin = bin(int(check_sum_character, 16))[2:].zfill(4*check_sum_length) # 4 for 128 bit, 2*4=8 for 256 ent
        
        return check_sum_bin
    
    def seed_binary(self, entropy, sk):
        
        check_sum = self.check_sum(entropy, sk)
        bin_entropy = self.entropy_to_binary(entropy)
        
        final_seed_bin  = bin_entropy + check_sum
        
        return final_seed_bin
    
    # Once we got full bin with check sum we can generate seed phrase
    @staticmethod
    def split_binary(bin_numbers):
    
        if len(bin_numbers) == 132:
            loop_length = 132
        else:
            loop_length = 264
            
        bin_splited = []
        for i in range(0,loop_length,11):
            bin_splited.append(bin_numbers[i : i+11])

        return bin_splited
    
    @staticmethod
    def calc_each_number(bin_splited, i):
    
        a = bin_splited[i]

        numbers = []
        for i in range(11):

            y = 10 - i
            number = int(a[i])*2**y
            numbers.append(number)

        sum_number = np.sum(numbers)

        return sum_number

    
    def calc_seed(self, bin_splited):

        seed_nrs = []
        for i in range(len(bin_splited)):

            number = self.calc_each_number(bin_splited, i)
            seed_nrs.append(number)

        return seed_nrs

    def generate_seed_phrase(self, entropy, sk):
        
        ### Compute all functions to gen seed phrase
        # 1. Calc final entropy with check_sum
        final_binary = self.seed_binary(entropy, sk)
        
        # 2. split binary number into special gropups dependend of number of bits
        bin_splited = self.split_binary(final_binary)
        
        # 3. Calculate seed numbers
        seed_nrs = self.calc_seed(bin_splited)
        
        # find equivalent numbers for words in bip39 dataset 
        seeds = []
        for i in range(len(seed_nrs)):
            seeds.append(bip39.iloc[seed_nrs[i]].values[0])

        seed_phrase = ' '.join(seeds)

        return seed_phrase
    
    
