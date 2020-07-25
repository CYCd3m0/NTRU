import ast
import base64
from math import log2
from Crypto.Util.number import long_to_bytes, bytes_to_long

from Parameters import Parameters
from Polynomial import Polynomial, inverse_3, inverse_2_power

# pub : (P, h)
# pri : (P, h, f, g)

PUBLIC_BEGIN_BLOCK = "-----BEGIN NTRU PUBLIC KEY-----"
PUBLIC_END_BLOCK = "-----END NTRU PUBLIC KEY-----"
PRIVATE_BEGIN_BLOCK = "-----BEGIN NTRU PRIVATE KEY-----"
PRIVATE_END_BLOCK = "-----END NTRU PRIVATE KEY-----"

class Moderate_Security(Parameters):
    def __init__(self):
        Parameters.__init__(self, 167, 3, 128, 61, 20, 18)

class Standard_Security(Parameters):
    def __init__(self):
        Parameters.__init__(self, 251, 3, 128, 50, 24, 16)

class Highest_Security(Parameters):
    def __init__(self):
        Parameters.__init__(self, 503, 3, 256, 216, 72, 55)

class NTRUKey():

    def __init__(self, P, h, f=None, g=None, fp=None, fq=None):
        """ Key parameters """
        self._P = P     # parameter set
        self._h = h     # public key
        self._f = f     # private key f
        self._g = g     # private key g
        self._fp = fp   # used for decryption
        self._fq = fq   # ensure correctness

    def encrypt(self, m):
        """ Type of m is byte """
        coeff_m = [int(x) for x in bin(bytes_to_long(m))[::-1][:-2]]
        m = Polynomial(coeff_m, len(coeff_m))

        e = b""
        if m._N <= self._P.get_N():
            r = self._P.generate_poly_r()
            c = (r.scale(self._P.get_p())*self._h+m) % self._P.get_q()  # Type of c is Polynomial
            tmp = c._coeff
            for i in tmp:
                e += i.to_bytes(1, byteorder='big', signed=True)        # Type of e is byte
            return e
        else:
            raise Exception("m is too large, must be equal or under size %d" % N)

    def decrypt(self, e):
        """ Type of e is byte """
        if self._f is None or self._g is None:
            raise Exception("Private key not found.")

        coeff_e = []
        for i in range(len(e)):
            coeff_e.append(int.from_bytes(bytes([e[i]]), byteorder='big', signed=True))
        e = Polynomial(coeff_e, len(coeff_e))

        if e._N <= self._P.get_N():
            if not self._fp:
                self._fp = inverse_3(self._f, self._P.get_N())
            if not self._fq:
                self._fq = inverse_2_power(self._f, self._P.get_N(), int(log2(self._P.get_q())))

            assert(self._h == self._fq * self._g)

            a = (self._f * e) % self._P.get_q()
            b = (self._fp * a) % self._P.get_p()

            m = 0
            for i in range(len(b._coeff)):
                m += (2**i) * b._coeff[i]

            return long_to_bytes(m)
        else:
            raise Exception("e is too large, must be equal or under size %d" % self._P.get_N())

    def export_public_key(self, file_name):
        content = "Parameters (N, p, q, df, dg, dr) = [" + str(self._P) + "]" + "\n" + "Coefficient of polynomial h = " + str(self._h._coeff)
        b64_content = base64.b64encode(content.encode()).decode()
        content = ""
        for i in range((len(b64_content)//64)+1):
            content += b64_content[i*64:(i+1)*64] + "\n"
        content = "\n" + content

        with open(file_name, 'w') as output_file:
            output_file.write(PUBLIC_BEGIN_BLOCK)
            output_file.write(content)
            output_file.write(PUBLIC_END_BLOCK)
            
    def export_private_key(self, file_name):
        if self.is_private():
            content = "Parameters (N, p, q, df, dg, dr) = [" + str(self._P) + "]" + "\n" + "Coefficient of polynomial h = " + str(self._h._coeff) + "\n" + "Coefficient of polynomial f = " + str(self._f._coeff) + "\n" + "Coefficient of polynomial g = " + str(self._g._coeff)
            b64_content = base64.b64encode(content.encode()).decode()
            content = ""
            for i in range((len(b64_content)//64)+1):
                content += b64_content[i*64:(i+1)*64] + "\n"
            content = "\n" + content

            with open(file_name, 'w') as output_file:
                output_file.write(PRIVATE_BEGIN_BLOCK)
                output_file.write(content)
                output_file.write(PRIVATE_END_BLOCK)
        else:
            raise Exception("Private key not found.")
    
    def is_private(self):
        return self._f is not None and self._g is not None
        
def generate_key(params = Standard_Security()):
    f = params.generate_poly_f()
    g = params.generate_poly_g()
    fp = inverse_3(f, params.get_N())

    r = 0
    if params.get_q() == 256 :
        r = 8
    elif params.get_q() == 128 :
        r = 7

    fq = inverse_2_power(f, params.get_N(), r)
    h = fq*g
    return NTRUKey(params, h, f, g, fp, fq)

def import_key(key_file):
    with open(key_file, 'r') as input_file:
        keys = input_file.read().replace("\n", "").replace(PUBLIC_BEGIN_BLOCK, "").replace(PUBLIC_END_BLOCK, "").replace(PRIVATE_BEGIN_BLOCK, "").replace(PRIVATE_END_BLOCK, "")
    keys = base64.b64decode(keys).decode()
    parameters_list = keys.split("\n")

    """ Dump parameters """
    params = parameters_list[0][35:] # len('Parameters (N, p, q, df, dg, dr) = ') = 35
    params = ast.literal_eval(params)
    params = Parameters(params[0],params[1],params[2],params[3],params[4],params[5])

    """ Dump polynomial h (public key) """   
    h = parameters_list[1][30:] # len('Coefficient of polynomial h = ') = 30
    h = Polynomial(ast.literal_eval(h), params.get_N())

    """ Dump polynomial f, g (private key) """
    f = g = None
    if len(parameters_list) == 4:
        f = parameters_list[2][30:]
        f = Polynomial(ast.literal_eval(f), params.get_N())
        g = parameters_list[3][30:]
        g = Polynomial(ast.literal_eval(g), params.get_N())

    if f and g:
        return NTRUKey(params, h, f, g)
    else:
        return NTRUKey(params, h)
