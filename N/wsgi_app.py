from qgb import py
U,T,N,F=py.importUTNF()

def app(env, start_response):
	'''  '''
    code=env['PATH_INFO'][1:]
    code=T.url_decode(code)
    if code.endswith('/'):code=code[:-1] # vercel
    
    start_response('200 OK', [('Content-Type','text/plain;charset=utf-8')])
    return [U.execResult(code,globals=py.globals(),locals=py.locals())]
