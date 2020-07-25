# NTRU

NTRUEncrypt module in Python3

## Requirements

```bash
pip3 install pycryptodome
```

## Functions

* ```NTRUEncrypt.generate_key(params)```

  * return NTRUKey entity , default params are Standard_Security
  
  * params support NTRUEncrypt.Moderate_Security() , NTRUEncrypt.Standard_Security() , NTRUEncrypt.Highest_Security()

* ```NTRUEncrypt.import_key(file)```

  * return NTRUKey entity according to file
  
* ```NTRUKey.encrypt(m)```

  * return ciphertext (Type bytes)

  * type of m should be bytes
  
* ```NTRUKey.decrypt(e)```

  * return plaintext (Type bytes)
  
  * type of e should be bytes
  
* ```NTRUKey.export_public_key(file)```

  * export Parameters and polynomial h to file
  
* ```NTRUKey.export_private_key(file)```

  *  export Parameters , polynomial h , polynomial f and polynomial g to file
  
## Reference

 * [pyNTRU](https://github.com/smarky7CD/PyNTRU)
 
 * https://upcommons.upc.edu/bitstream/handle/2099.1/8522/memoria.pdf
 
