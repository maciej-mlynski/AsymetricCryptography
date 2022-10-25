from key_generators import recoverKeys

Your_seed_phrase = 'stomach convince expand sunset require morning quit bacon early romance old future burden great moon melt hover squeeze ripple helmet zero spatial when media'

retreveKey = recoverKeys.RetreveSK()

print(retreveKey.calc_entropy(Your_seed_phrase, True))

