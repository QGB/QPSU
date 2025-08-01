#coding=utf-8
import sys #endswith 是为了适配qgb处于另外一个包内的情况
if __name__.endswith('qgb.N.CA'):from .. import py
else:
    from pathlib import Path
    gsqp=Path(__file__).parent.parent.parent.absolute().__str__()
    if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
    from qgb import py
U,T,N,F=py.importUTNF()

def generate_consistent_ecdsa_key(secexp,curve='NIST256p',dir='C:/test/ssh/'):
    ''' pip install ecdsa  
在不同的机器上，U.generate_ecdsa_by_secexp 相同的secexp生成的 privateKey 文件内容不完全相同（#todo），但是都可以正常连接

from qgb.N import CA;CA.generate_consistent_ecdsa_key() 输出相同文件 ; 
       '''
    import ecdsa,hashlib,base64
    curve = getattr(ecdsa, curve)
    # 强制使用相同的哈希函数和参数
    sk = ecdsa.SigningKey.from_secret_exponent(
        secexp=secexp,
        curve=curve,
        hashfunc=hashlib.sha256  # 固定哈希函数
    )

    # 获取DER编码
    der_encoded = sk.to_der()   # 注意：这里没有参数

    # 将DER转换为PEM格式（手动）
    # 对DER进行base64编码
    b64_encoded = base64.b64encode(der_encoded).decode('ascii')
    # 每64个字符插入一个换行
    b64_lines = [b64_encoded[i:i+64] for i in range(0, len(b64_encoded), 64)]
    b64_with_newlines = '\n'.join(b64_lines)
    # 添加PEM头部和尾部
    pem_encoded = '-----BEGIN EC PRIVATE KEY-----\n' + b64_with_newlines + '\n-----END EC PRIVATE KEY-----'
    return pem_encoded,F.write(f"{dir}privateKey_{curve}_{secexp}.pem",pem_encoded)



def get_certificate_expiration(crt_path):
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend
    # from datetime import datetime
    with open(crt_path, 'rb') as crt_file:
        crt_data = crt_file.read()
        certificate = x509.load_pem_x509_certificate(crt_data, default_backend())
        expiration_date = certificate.not_valid_after
        return expiration_date  # return type datetime.datetime
get_crt_date=get_crt_expiration_date=get_certificate_expiration

def secexp_to_bytes_len_32(secexp):
    # Ensure secexp is 32 bytes long
    if isinstance(secexp, int):
        # Convert integer to bytes
        secexp = secexp.to_bytes(32, byteorder='little')
    elif isinstance(secexp, bytes):
        if len(secexp) < 32:
            # Pad with \x00 to make it 32 bytes long
            secexp = b'\x00' * (32 - len(secexp)) + secexp
        elif len(secexp) > 32:
            raise ValueError("The secret exponent must be 32 bytes long for Ed25519.")
    else:
        raise ValueError("The secret exponent must be an integer or a byte string.")
    return secexp

def generate_ed25519_PEM_format_by_secexp(secexp=None, curve='Ed25519', comment="", dir='C:/test/ssh/', return_pub=False):
    '''
Generate Ed25519 key pair using the provided secret exponent or a new one if not provided.
    
for b	
    '''
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    import base64
    U, T, N, F = py.importUTNF()

    if py.istr(secexp):
        comment = T.file_legalized(secexp)
        secexp = py.eval(secexp)

    if not comment:
        comment = py.str(secexp)

    if secexp is None:
        # Generate a new private key if secexp is not provided
        private_key = Ed25519PrivateKey.generate()
    else:
        secexp = secexp_to_bytes_len_32(secexp)
        private_key = Ed25519PrivateKey.from_private_bytes(secexp)

    public_key = private_key.public_key()

    # Serialize the private key to PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serialize the public key to PEM format
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(f"{dir}privateKey_{curve}_{comment}.pem", "wb") as f:
        f.write(private_pem)

    with open(f"{dir}publicKey_{curve}_{comment}.pem", "wb") as f:
        f.write(public_pem)

    if return_pub:
        return public_pem.decode()

    return private_key, public_key
    

def generate_rsa_PEM_format_by_secexp(secexp=None,secexp_n=0,key_size=2048, comment="", dir='C:/test/ssh/', return_pub=False):
    '''
    Generate RSA key pair using the provided secret exponent or a new one if not provided.
    '''
    import rsa.prime
    # nbits = key_size
    # m = secexp
     
    def generate_prime(nbits):
        nonlocal secexp_n
        print('generate_prime',nbits)
        while True:
            value = secexp + secexp_n
            value |= 1 << (nbits - 1)
            value |= 1
            if rsa.prime.is_prime(value):
                print(secexp_n)
                break
            secexp_n += 1   
        return value

    # Generate the keys
    (p, q, e, d) = rsa.key.gen_keys(key_size, generate_prime)

    # Create the key objects
    n = p * q
    public_key = rsa.PublicKey(n, e)
    private_key = rsa.PrivateKey(n, e, d, p, q)

    # Serialize the private key to PEM format
    private_pem = private_key.save_pkcs1(format='PEM')

    # Serialize the public key to PEM format
    public_pem = public_key.save_pkcs1(format='PEM')

    with open(f"{dir}privateKey_RSA_{comment}.pem", "wb") as f:
        f.write(private_pem)

    with open(f"{dir}publicKey_RSA_{comment}.pem", "wb") as f:
        f.write(public_pem)

    if return_pub:
        return public_pem.decode()

    return private_key, public_key

