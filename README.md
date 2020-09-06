# NTRU

NTRUEncrypt module in Python3

## Requirements

```bash
pip3 install pycryptodome
```

## Class attribute

* Polynomial

  * _coeff

  * _N

<br/>

* NTRUKey

  * _P
  > parameter set

  * _h

  * _f

  * _g

  * _fp

  * _fq

## Functions

* ```NTRUEncrypt.generate_key(params)```

  * return NTRUKey entity , default params are Standard_Security
  
  * params support

    * NTRUEncrypt.Moderate_Security()

    * NTRUEncrypt.Standard_Security()

    * NTRUEncrypt.Highest_Security()

<br/>

* ```NTRUEncrypt.import_key(file)```

  * return NTRUKey entity according to file
  
<br/>

### For NTRUKey

* ```NTRUKey.encrypt(m)```

  * return ciphertext (Type bytes)

  * type of m should be bytes
  
<br/>

* ```NTRUKey.encrypt_to_poly(m)```

  * return ciphertext (Type list)

  * type of m should be bytes

<br/>

* ```NTRUKey.decrypt(e)```

  * return plaintext (Type bytes)
  
  * type of e should be bytes
  
<br/>

* ```NTRUKey.decrypt_from_poly(e)```

  * return plaintext (Type bytes)
  
  * type of e should be list

<br/>

* ```NTRUKey.export_public_key(file)```

  * export Parameters and polynomial h to file

<br/>

* ```NTRUKey.export_private_key(file)```

  *  export Parameters , polynomial h , polynomial f and polynomial g to file

<br/>

## Reference

  * [pyNTRU](https://github.com/smarky7CD/PyNTRU)

  * [NTRU software implementation for constrained devices](https://upcommons.upc.edu/bitstream/handle/2099.1/8522/memoria.pdf)

  * [Almost Inverse Algorithm](https://assets.onboardsecurity.com/static/downloads/NTRU/resources/NTRUTech014.pdf)
