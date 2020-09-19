import os
import sys
sys.path.append('./NTRU')
import NTRUEncrypt

# generate , export , import
cipher = NTRUEncrypt.generate_key(NTRUEncrypt.Highest_Security())
cipher.export_public_key('test.pub')
cipher.export_private_key('test.pri')

pub_key = NTRUEncrypt.import_key('test.pub')
pri_key = NTRUEncrypt.import_key('test.pri')
assert(vars(cipher._P) == vars(pri_key._P))
assert(vars(cipher._P) == vars(pub_key._P))
print('Success !')


# encrypt , decrypt
m = os.urandom(16)
c = pub_key.encrypt(m)
m2 = pri_key.decrypt(c)
assert(m == m2) , 'bad NTRU key'
print('Success !')


# encrypt_to_poly , decrypt_from_poly
m = os.urandom(16)
c = pub_key.encrypt_to_poly(m)
m2 = pri_key.decrypt_from_poly(c)
assert(m == m2) , 'bad NTRU key'
print('Success !')
