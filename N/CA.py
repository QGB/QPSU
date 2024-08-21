#coding=utf-8
import sys #endswith 是为了适配qgb处于另外一个包内的情况
if __name__.endswith('qgb.N.CA'):from .. import py
else:
	from pathlib import Path
	gsqp=Path(__file__).parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	from qgb import py
U,T,N,F=py.importUTNF()


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