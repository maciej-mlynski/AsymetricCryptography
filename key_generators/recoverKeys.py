'''
User can retreve his secret key by seed phrase, becouse it can provide by some calculation to entropy. 
Entropy is key thing to find out what secret key is. We just need to use the hash method (sha-256) again.
Hypothetically this is only one way to retreve secret key.

Beyond that seed phrase can be use to sign and decrypt message. Obviously becouse seed phrase lead to secret key.
'''

from itertools import combinations
import pandas as pd
bip39 = pd.read_csv('../AsymetricCryptography/BIP-39/bip39')

from hash_method import SHA_256

class RetreveSK:
    
    # Convert seed words into seed number base on bip38 words index
    @staticmethod
    def find_number_repr_of_word(seed_phrase):
        seed_nrs = []
        for seed in seed_phrase.split(' '):
            seed_nr = bip39.index[bip39['BIP-39 words'] == seed][0]
            seed_nrs.append(seed_nr)
        return seed_nrs
    
    # Find numbers that added together form single number in seed phrase
    # eg. seed word is tongue which has index of 1827 ->
    # -> thing is to find the combination of numbers from the list (numbers) ->
    # that their sum is equal to 1827
    @staticmethod
    def find_sum(numbers, target):
        
        for i in range(len(numbers), 0, -1):
            for seq in combinations(numbers, i):
                if sum(seq) == target:
                    return seq
    
    # give 1 if single seed nr is in the list of all number
    # else: 0
    @staticmethod
    def find_bin_repres(numbers, selected_numbers):
        num_to_bin = []
        for i in range(len(numbers)):
            if numbers[i] in selected_numbers:
                x = '1'
            else:
                x = '0'
            num_to_bin.append(x)

        return int("".join(num_to_bin))
    
    # calculate entropy base on 3 previous method for all words in seed phrase
    def calc_entropy(self, seed_phrase, in_hex):
        
        seed_nrs = self.find_number_repr_of_word(seed_phrase)
        
        # This numbers are always the same for BIP39
        # 1024 = 1*2**10, 512 = 1*2**9,..., 1*2**0
        numbers = [1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1]
        
        seed_binary = []
        for seed_nr in seed_nrs:
            # find numbers that create each seed number
            each_nrs = self.find_sum(numbers, seed_nr)
            
            # convert to binary in specific way
            # eg.: if the sum contains numbers: 1024, 128, 8, 2, 1 ->
            # then in binary it is: 10010001010, becouse
            # 1024 in each_nrs -> 1, 512, 256 not in each nrs -> 00, 128 in -> 1, 64, 32, 16 ->0 etc.
            bin_repr = self.find_bin_repres(numbers, each_nrs)
            bin_repr = str(bin_repr)
            
            # in case len is less than 11 -> add zeros in front
            if len(bin_repr) < 11:
                bin_repr =  '0'*(11-len(bin_repr)) + bin_repr

            seed_binary.append(bin_repr)
            
        seed_binary = int("".join(seed_binary))
        bin_entr = str(seed_binary)
        
        # convert to int and cut last 1 or 2 bit/s
        final_bin_entr = int(bin_entr[:-8], 2)
        
        if len(bin_entr) < 256:
            
            final_bin_entr = int(bin_entr[:-4],2)
        
        sk = int(SHA_256.double_sha256(hex(final_bin_entr)[2:]), 16)
        
        if in_hex:
            return hex(sk)
        
        return sk

