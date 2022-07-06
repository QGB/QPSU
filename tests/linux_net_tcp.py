# -*- coding: utf-8 -*-
import re
import sys,pathlib            # *.py  /tests /qgb   /[gsqp]
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()



net_tcp=sys.argv[1] if len(sys.argv)>1 else '/proc/net/tcp'
if not [i for i in net_tcp if i not in '0123456789']:
	net_tcp='/proc/{}/net/tcp'.format(net_tcp)

def process_file(procnet):
	sockets = procnet.split('\n')[1:-1]
	return [line.strip() for line in sockets]

def split_every_n(data, n):
	return [data[i:i+n] for i in range(0, len(data), n)]

def convert_linux_netaddr(address):

	hex_addr, hex_port = address.split(':')

	addr_list = split_every_n(hex_addr, 2)
	addr_list.reverse()

	addr = ".".join(map(lambda x: str(int(x, 16)), addr_list))
	port = str(int(hex_port, 16))

	return "{}:{}".format(addr, port)

def format_line(data):
	d={
		'seq'    :5,
		'uid'    :9,
		'local'  :15,
		'remote' :68,
		'timeout':3,
		'inode'  :11,
	}
	row=[]
	for k,size in d.items():
		v=data[k]
		if k in ['local','remote']:
			if ':' in v:
				ip,port=v.split(':')
				ip=N.ip_location(reverse_ip=1,ip=ip,size=size)
				port=U.IntRepr(port,size=1+5)
			else:
				ip,port=U.StrRepr(k,size=size),U.StrRepr(k[0]+'_port',size=1+5)
				
			row.append(ip)	
			row.append(port)	
			continue
		row.append( U.StrRepr(v,size=size) )	
	return row	
	# return (("%(seq)-4s %(uid)5s %(local)25s %(remote)25s %(timeout)8s %(inode)8s" % data) )#+ "\n"

with open(net_tcp) as f:
	sockets = process_file(f.read())

columns = ("seq", "uid", "inode", "local", "remote", "timeout")
title = dict()
for c in columns:
	title[c] = c

rv = []
for info in sockets:
	_ = re.split(r'\s+', info)

	_tmp = {
		'seq': _[0],
		'local': convert_linux_netaddr(_[1]),
		'remote': convert_linux_netaddr(_[2]),
		'uid': _[7],
		'timeout': _[8],
		'inode': _[9],
	}
	rv.append(_tmp)
def main(return_title=True):
	# from qgb import py,U
	r=[]
	if len(rv) > 0:
		if return_title:
			r.append(format_line(title))

		for _ in rv:
			r.append(format_line(_))
	return r

if __name__ == '__main__':
	# from pprint import pprint
	U.pprint(main())

		
		