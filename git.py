#coding=utf-8
import sys,pathlib
# 要修改路径，框选两行，一起删除 *.py /qgb   /[gsqp]  
gsqp=pathlib.Path(__file__).absolute().parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
# 上个版本问题： print(dir(py),py) #['__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__'] <module 'py' (namespace)>
U,T,N,F=py.importUTNF()

import os,sys,shutil

try:
    import dulwich
    from dulwich import client,index,repo,porcelain
    from dulwich.client import get_transport_and_path_from_url #    return (<dulwich.client.SSHGitClient at 0x23218db7f88>, '/qgb/xxnet.git')
except Exception as e:
    print('pip install dulwich paramiko #',e)
try:
    import paramiko
except Exception as e:
    print('pip install dulwich paramiko #',e)
# from six.moves import urllib
# opener = urllib.request.build_opener()
# headers={'Authorization':F.read('Authorization')}
# opener.addheaders = py.list(headers.items())
# urllib.request.install_opener(opener)
grepo=U.get('git.repo')

def github_lfs_upload(filename, repo, token, branch='master', proxies=None, verbose=True, verify_ssl=False):
    ''' 彻底修复域名粘连并支持代理的 LFS 上传函数 '''
    import os, hashlib, requests, json, base64, urllib3; urllib3.disable_warnings() # 导入库
    res = {"success": False, "message": "", "oid": "", "size": 0} # 初始化
    try:
        f_size = os.path.getsize(filename); sha256 = hashlib.sha256() # 获取大小
        with open(filename, "rb") as f: # 分块计算哈希
            for chunk in iter(lambda: f.read(4096), b""): sha256.update(chunk)
        oid = sha256.hexdigest(); r_path = repo.strip("/"); res["oid"], res["size"] = oid, f_size # 规范路径
        if verbose: print(f"🚀 哈希: {oid}\n📡 目标: {repo} [{branch}]") # 打印状态
        # 1. LFS Batch 授权 (核心修正：确保域名后有斜杠 / 避免粘连)
        batch_url = f"https://github.com/{r_path}.git/info/lfs/objects/batch" # 修正拼接
        h = {"Accept": "application/vnd.git-lfs+json", "Content-Type": "application/vnd.git-lfs+json", "Authorization": f"token {token}", "User-Agent": "git-lfs/3.3.0"} 
        payload = {"operation": "upload", "transfers": ["basic"], "objects": [{"oid": oid, "size": f_size}]} # 载荷
        res_b = requests.post(batch_url, json=payload, headers=h, proxies=proxies, verify=verify_ssl, timeout=30) # 授权请求
        if verbose: print(f"  [Batch] Status: {res_b.status_code}") # 调试信息
        if res_b.status_code != 200: raise RuntimeError(f"Batch授权失败: {res_b.text}") # 抛错
        # 2. 二进制上传 (如果 LFS 服务器没有此文件)
        action = res_b.json()['objects'][0].get('actions', {}).get('upload') # 提取动作
        if action:
            if verbose: print("  [Binary] 正在上传流...") # 状态
            with open(filename, 'rb') as fs: # 流式上传
                res_put = requests.put(action['href'], data=fs, headers=action.get('header', {}), proxies=proxies, timeout=900, verify=verify_ssl)
                if verbose: print(f"  [Binary] Status: {res_put.status_code}") # 调试信息
        # 3. 提交指针文件 (必须包含 /repos/ 关键字)
        ptr = f"version https://git-lfs.github.com\noid sha256:{oid}\nsize {f_size}\n" # 标准指针内容
        ptr_url = f"https://api.github.com/repos/{r_path}/contents/{os.path.basename(filename)}" # API 路径
        auth = {"Authorization": f"token {token}", "User-Agent": "Py-QGB"} # 认证
        get_r = requests.get(ptr_url, headers=auth, proxies=proxies, verify=verify_ssl) # 查旧 SHA
        ptr_data = {"message": f"LFS upload {os.path.basename(filename)}", "content": base64.b64encode(ptr.encode()).decode(), "branch": branch}
        if get_r.status_code == 200: ptr_data["sha"] = get_r.json()["sha"] # 带上 sha 执行更新
        final_r = requests.put(ptr_url, json=ptr_data, headers=auth, proxies=proxies, verify=verify_ssl) # 提交指针
        if verbose: print(f"  [Pointer] Status: {final_r.status_code}") # 调试信息
        if final_r.status_code in [200, 201]: res["success"] = True; res["message"] = "上传成功" # 标记完成
    except Exception as e: res["message"] = str(e); print(f"❌ 失败: {e}") # 记录错误
    return res # 返回结果

def gitea_upload(filename, repo, token, branch='master', commit_msg='', safe_filename='', BASE_URL="https://xxx/6080",**ka):
    ''' 适配 Gitea API 上传文件（强制补齐 api/v1 路径）
mkdir /tmp/gitea
!podman run -p 6080:3000 -p 10022:22 -v /tmp/gitea:/data -e GITEA__server__ROOT_URL=https://xxx.com/6080/ -e GITEA__server__HTTP_ADDR=0.0.0.0 -e GITEA__server__HTTP_PORT=3000 docker.io/gitea/gitea:latest

#注意没有6080
sed -i 's|^ROOT_URL *=.*|ROOT_URL = https://xxx.com|' /tmp/gitea/gitea/conf/app.ini    
# 1. 允许仓库上传大文件
sed -i '/\[repository\.upload\]/a FILE_MAX_SIZE = 500' /tmp/gitea/gitea/conf/app.ini
# 2. 允许 LFS 大文件
sed -i '/\[lfs\]/a MAX_FILE_SIZE = 524288000' /tmp/gitea/gitea/conf/app.ini
# 3. 增大 HTTP 请求体限制
sed -i '/\[server\]/a HTTP_MAX_CONTENT_LENGTH = 524288000' /tmp/gitea/gitea/conf/app.ini

    '''
    import requests, json, base64, os, urllib3; urllib3.disable_warnings() # 导入库并禁用警告
    from qgb import U, T, F # 保持库习惯
    path = T.url_encode(safe_filename or os.path.basename(filename)) # 编码文件名
    # 核心修正：无论参数是否带 v1，此处通过 rstrip 保证路径拼接为 .../6080/api/v1/repos/...
    api_url = f"{BASE_URL.rstrip('/')}/api/v1/repos/{repo}/contents/{path}"
    commit_msg = commit_msg or f"Upload {os.path.basename(filename)} at {U.stime()}" # 提交信息
    with open(filename, 'rb') as f: content_b64 = base64.b64encode(f.read()).decode('utf-8') # 读取并编码文件
    data = {"branch": branch, "message": commit_msg, "content": content_b64} # 构建请求体
    headers = {'Authorization': f'token {token}', 'Content-Type': 'application/json', 'Accept': 'application/json'} # 认证头
    print(f"正在上传: {os.path.basename(filename)} 到 {repo}...") # 打印状态
    # timeout=600 解决大文件 SSLEOFError，verify=False 忽略证书
    res = requests.post(api_url, data=json.dumps(data), headers=headers, timeout=600, verify=False,**ka)
    if res.status_code == 201: print(f" 上传成功！") # Gitea 创建成功返回 201
    else: print(f" 失败 {res.status_code}: {res.text}") # 打印错误详细信息
    return res # 返回响应对象
# gitea_upload(filename='C:/Users/Administrator/Documents/energetic/.gitignore',repo='a/energetic',token='16059ac8367da45cf626cc2612cd65b6c522868d')

def github_force_empty(repo='', token=None, branch='master', proxies=None, **ka):
    ''' 强制清空 Github 仓库（删除所有文件并重置历史），等效 git push -f 到空仓库 '''
    import requests, json, urllib3 # 导入必要库
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # 忽略SSL警告
    print_requests = U.get_duplicated_kargs(ka, 'show', 'print', 'p', 'print_req', 'print_requests', default=False) # 获取打印参数
    if not repo or not token: repo, token = U.get_or_input('repo,token', default='', type=py.eval) # 获取配置
    token = token.strip() # 去空格
    if not token.startswith('token '): token = 'token ' + token # 格式化token
    headers = {'Authorization': token, 'Accept': 'application/vnd.github.v3+json', 'User-Agent': 'PyGithub/Python'} # 设置请求头
    # 步骤1：定义Git逻辑上的空树哈希
    empty_tree_sha = "4b825dc642cb6eb9a060e54bf8d69288fbee4904" # Git预定义的空目录SHA
    # 步骤2：创建孤立的空Commit
    commit_url = f'https://api.github.com/repos/{repo}/git/commits' # 提交接口
    commit_data = json.dumps({'message': f'Force Empty by qgb {U.stime()}', 'tree': empty_tree_sha, 'parents': []}) # 无父节点即清空历史
    req_ka = {'headers': headers, 'proxies': proxies, 'verify': False, 'timeout': 20} # 统一请求参数
    res_commit = requests.post(commit_url, data=commit_data, **req_ka) # 发送创建请求
    if print_requests: print(f'Create Commit: {res_commit.status_code}\n{res_commit.text}') # 调试输出
    new_commit_sha = res_commit.json()['sha'] # 提取新提交的SHA
    # 步骤3：强制更新Ref指向新Commit
    ref_url = f'https://api.github.com/repos/{repo}/git/refs/heads/{branch}' # 分支引用接口
    update_data = json.dumps({'sha': new_commit_sha, 'force': True}) # 必须开启force
    res_update = requests.patch(ref_url, data=update_data, **req_ka) # 强制覆盖
    if print_requests: print(f'Update Ref: {res_update.status_code}\n{res_update.text}') # 调试输出
    # print(res_update,res_update.text) # 返回200即成功
    return res_update # 返回最终操作结果



def ssh_T(host='github.com',port=22,username='git',private_key='',proxy=0,cmd=''):
    ''' -T 禁用伪 tty 分配。Disable pseudo-tty allocation.
ssh.connect(
    hostname,
    port=22,
    username=None,
    password=None,
    pkey=None,
    key_filename=None,
    timeout=None,
    allow_agent=True,
    look_for_keys=True,
    compress=False,
    sock=None,
    gss_auth=False,
    gss_kex=False,
    gss_deleg_creds=True,
    gss_host=None,
    banner_timeout=None,
    auth_timeout=None,
    gss_trust_dns=True,
    passphrase=None,
    disabled_algorithms=None,
)
'''    
    import paramiko
    import socks
    sock=socks.socksocket()
    if proxy:
        sock.set_proxy(
            proxy_type=socks.SOCKS5,
            addr="127.0.0.1",
            port=21080,
            # username="blubbs",
            # password="blabbs"
        )
    sock.connect((host,port)) #None
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=host, username=username,key_filename=private_key, sock=sock)
    except Exception as e:
        return py.No(e)
    
    channel = ssh.get_transport().open_session(timeout=1000)
    
    from paramiko.message import Message
    from paramiko.common import  cMSG_CHANNEL_REQUEST
    m = Message()
    m.add_byte(cMSG_CHANNEL_REQUEST)
    m.add_int(channel.remote_chanid)
    m.add_string("shell")
    m.add_boolean(True)
    channel.transport._send_user_message(m)
    
    bo=be=b''
    for i in range(10):
        ready=channel.recv_ready(),channel.recv_stderr_ready()
        print(U.stime(),ready)
        if py.any(ready):
            if channel.recv_ready():
                bo=channel.recv(4096)
            if channel.recv_stderr_ready():
                be=channel.recv_stderr(4096)
            return bo+be
            break
        U.sleep(0.2)
    else:
        print(U.stime(),'timeout! 10*0.2 ')
    
    
    return sock,ssh,channel

    return sock,ssh


    # with open_private_key(private_key) as fpkey:
        # pkey=paramiko.RSAKey.from_private_key(fpkey, password=None) #private_key_password

        # if 'git@' not in repo_path:
            # raise py.NotImplementedError("'git@' not in repo_path")
            # repo_path
        
        # ParamikoSSHVendor(pkey=pkey)


def clone(url,path=None):
    client, target = dulwich.client.get_transport_and_path(url) #c , 'user/repo'
    if not path:
        if target.endswith('.git'):
            target=target[:-4]
        path=target
    path=F.mkdir(path)
    ls=F.ls(path)
    if len(ls)>1: #skip .git
        return py.No('Not empty dir:'+path,ls)
    if len(ls)==1:
        r = dulwich.repo.Repo(path)
    else:    
        r = dulwich.repo.Repo.init(path)
    print(U.stime(),'fetching url...')
    remote_refs = client.fetch(url, r)
    r[b"HEAD"] = remote_refs[b"HEAD"]

    print(U.stime(),'build_index_from_tree ...')
    index.build_index_from_tree(r.path, r.index_path(), r.object_store, r[b'HEAD'].tree)
    
    r.close()
    return path,r

def up(url,path=None,commit_msg=None,username=None,password=None,branch='master',retry=3,**ka):
    r'''
porcelain.push(repo.path,"https://wrong_name@e.coding.net/...",'master',username='correct_name',password=_) ## 也会GitProtocolError: unexpected http resp 401 for

porcelain.push(repo.path,"https://http://e.coding.net/...",'master',username='correct_name',password=_)  #  OK!    


C:/QGB/babun/cygwin/bin/qgb/ adding ... 2021-12-07__13.20.51__.479
commit ... 2021-12-07__13.20.51__.559
push ... 2021-12-07__13.20.51__.573
  File "C:/QGB/babun/cygwin/bin\qgb\git.py", line 106, in up
    rp=push_with_key(repo.path,url,**ka)
  File "C:/QGB/babun/cygwin/bin\qgb\git.py", line 231, in push_with_key
    progress=errstream.write)
  File "C:\QGB\Anaconda3\lib\site-packages\dulwich\client.py", line 789, in send_pack
    proto, unused_can_read, stderr = self._connect(b'receive-pack', path)
  File "C:\QGB\Anaconda3\lib\site-packages\dulwich\client.py", line 1410, in _connect
    **kwargs)
  File "C:\QGB\Anaconda3\lib\site-packages\dulwich\contrib\paramiko_vendor.py", line 103, in run_command
    client.connect(**connection_kwargs)
  File "C:\QGB\Anaconda3\lib\site-packages\paramiko\client.py", line 349, in connect
    retry_on_signal(lambda: sock.connect(addr))
  File "C:\QGB\Anaconda3\lib\site-packages\paramiko\util.py", line 283, in retry_on_signal
    return function()
  File "C:\QGB\Anaconda3\lib\site-packages\paramiko\client.py", line 349, in <lambda>
    retry_on_signal(lambda: sock.connect(addr))
    '''
    global grepo
    if ':' not in url:
        url='https://'+url
    if 'git@' not in url:
        domain=T.netloc(url)
        if not username:
            username=U.get_or_input(domain+'_git.username')
        ka['username']=username
        if not password:
            password=U.get_or_input(domain+'_git.password')
        ka['password']=password
    if not 'refspecs' in ka:
        ka['refspecs']=branch
    if not path and '/qpsu' in url.lower():
        path=U.get_qpsu_dir()
    if not path:    
        _client, target = dulwich.client.get_transport_and_path(url) 
        if target.endswith('.git'):
            target=target[:-4]
        path=target
        
    path=F.auto_path(path)
    ls=[i[len(path):] for i in F.ls(path,d=0,f=1,r=1)]
    if len(ls) < 1:
        return py.No('Not contains .git dir:'+path,ls)

    repo=dulwich.repo.Repo(path)
    U.pln(path,'adding ...',U.stime())
    repo.stage(['git.py'],)
    dulwich.porcelain.add(repo.path)  #TODO  pwd 必须在当前repo目录下 ，否则
# 1-> 212     treepath = os.path.relpath(path, repopath)
    # 213     if treepath.startswith(b'..'):
    # 214         raise ValueError('Path not in repo')
# ipdb> !(path, repopath)
# (b'C:\\test\\www\\png\\0010005960.png', b'C:/QGB/babun/cygwin/bin/qgb/')        
    
    U.pln('commit ...',U.stime())

    bhash,commit_msg=commit(repo,commit_msg)                    
    r= bhash,commit_msg, ka
    repo.close()
    U.pln('push ...',U.stime())
    try:
        #repo.path == 'C:/QGB/babun/cygwin/bin/qgb/'
        if 'git@' in url:
            rp=push_with_key(repo_path=repo.path,remote=url,retry=retry,**ka)
            if not rp:return rp
        else:
            dulwich.porcelain.push(repo.path, url , **ka )
        
    except Exception as e:
        U.print_tb()
        U.v.dulwich.porcelain.push(repo.path, url , **ka )
        r=py.No(e,r)
    return r
    # porcelain.push(repo.repo.path, result.url, branch_name, errstream=outstream)                    
    
def commit(repo,commit_msg):
    if not commit_msg:
        commit_msg='dulwich_'+U.stime()
    if not py.isbytes(commit_msg):
        commit_msg=commit_msg.encode('utf-8')
            
    index = repo.open_index()
    new_tree = index.commit(repo.object_store)
    if new_tree != repo[repo.head()].tree:
        bhash=repo.do_commit(commit_msg, tree=new_tree)
        return bhash,commit_msg
    else:
        return b'',py.No("Empty commit!")

def log(max_entries=11,repo=None):
    
    return dulwich.porcelain.log(max_entries=max_entries) 
    
    
def open_private_key(f,):
    ''' 
paramiko.RSAKey.from_private_key(open_private_key(f),)  == <paramiko.rsakey.RSAKey at 0x23218fda648> '''
    if py.isfile(f):
        file=f
    elif not py.istr(f):
        raise py.ArgumentError('key f type must file or str',f)
    elif F.exist(f):
        file=py.open(f)
    elif py.len(f)<256 and 'PRIVATE KEY' not in f.upper():
        raise py.ArgumentError('private_key f str format Error ! Or [%s] not exist'%f)
    else:
        from io import StringIO
        file=StringIO(f)
    return file    
    
def push_with_key(repo_path,remote="ssh://git@github.com:22/QGB/QPSU.git",private_key='',refspecs='master',errstream=getattr(sys.stderr, 'buffer', None),private_key_password=None,retry=3):
    r''' #important#    三引号string中不能出现 \util 这种字符（常见于路径）
# 会导致 SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 1-2: truncated \uXXXX escape 错误
# 最好 引号前加r 强制用 raw-string
    
push ... 2021-04-15__06.26.44__.288
  File "C:/QGB/babun/cygwin/bin\qgb\git.py", line 106, in up
    push_with_key(repo.path,url,**ka)
  File "C:/QGB/babun/cygwin/bin\qgb\git.py", line 205, in push_with_key
    progress=errstream.write)
  File "C:\QGB\Anaconda3\lib\site-packages\dulwich\client.py", line 789, in send_pack
    proto, unused_can_read, stderr = self._connect(b'receive-pack', path)
  File "C:\QGB\Anaconda3\lib\site-packages\dulwich\client.py", line 1410, in _connect
    **kwargs)
  File "C:\QGB\Anaconda3\lib\site-packages\dulwich\contrib\paramiko_vendor.py", line 103, in run_command
    client.connect(**connection_kwargs)
  File "C:\QGB\Anaconda3\lib\site-packages\paramiko\client.py", line 349, in connect
    retry_on_signal(lambda: sock.connect(addr))
  File "C:\QGB\Anaconda3\lib\site-packages\paramiko\util.py", line 283, in retry_on_signal
    return function()
  File "C:\QGB\Anaconda3\lib\site-packages\paramiko\client.py", line 349, in <lambda>
    retry_on_signal(lambda: sock.connect(addr))
Out[26]: 'C:/QGB/babun/cygwin/bin/qgb/'
 '''
    from dulwich.contrib.paramiko_vendor import ParamikoSSHVendor
    import dulwich.porcelain
    from dulwich.protocol import (
        Protocol,
        ZERO_SHA,
    )
    from dulwich.objectspec import (
        parse_commit,
        parse_object,
        parse_ref,
        parse_reftuples,
        parse_tree,
        )
    from dulwich.errors import (
        GitProtocolError,
        NotGitRepository,
        SendPackError,
        # UpdateRefsError,
    )    
    DEFAULT_ENCODING = 'utf-8'    
    selected_refs = []
    
    if not private_key:
        private_key=U.get_or_set('id_rsa',F.get_home()+'.ssh/id_rsa' )
    private_key=U.set('id_rsa',private_key)
    
    with open_private_key(private_key) as fpkey, dulwich.porcelain.open_repo_closing(repo_path) as r:
        def update_refs(refs):
            selected_refs.extend(parse_reftuples(r.refs, refs, refspecs))
            new_refs = {}
            # TODO: Handle selected_refs == {None: None}
            for (lh, rh, force) in selected_refs:
                if lh is None:
                    new_refs[rh] = ZERO_SHA
                else:
                    new_refs[rh] = r.refs[lh]
            return new_refs
        
        import paramiko
        skey=fpkey.read()
        fpkey.seek(0)
        if 'RSA' in skey:
            pkey=paramiko.RSAKey.from_private_key(fpkey, password=private_key_password)
        else:
            pkey=paramiko.ECDSAKey.from_private_key(fpkey, password=private_key_password)
            
        if 'git@' not in repo_path:
            # raise py.NotImplementedError("'git@' not in repo_path")
            repo_path
        
        client, path=dulwich.client.get_transport_and_path( remote, vendor=ParamikoSSHVendor(pkey=pkey))
        
        err_encoding = getattr(errstream, 'encoding', None) or DEFAULT_ENCODING
        remote_location_bytes = client.get_url(path).encode(err_encoding)
        #b'ssh://git@github.com:22/QGB/QPSU.git'
        try:
            client.send_pack(
                path, update_refs,
                generate_pack_data=r.object_store.generate_pack_data,
                progress=errstream.write)
            # print(remote_location_bytes)
            errstream.write(
                b"Push to " + remote_location_bytes + b" successful.\n")
            errstream.flush()    # 与 stdout 混合打印时 ，顺序可能不同
        except ( SendPackError) as e:#UpdateRefsError,
            errstream.write(b"Push to " + remote_location_bytes +
                            b" failed -> " + e.message.encode(err_encoding) +
                            b"\n")
            return py.No(e)
        finally:
            errstream.flush()
        return client
        # return r.path,remote_location_bytes
        
GITHUB_TOKEN=py.No('auto get_or_set_input')

def get_github_repo_directory_as_list(url,token=GITHUB_TOKEN,return_object=True,return_str=False,return_fullpath=True,**ka):
    '''pip install pygithub'''
    import github
    if not token:
        token=U.get_or_set_input('github.token')
    g=github.Github(token)
    d=T.regex_match_named(url,T.RE_GIT_URL)
    if not d:return d
    repo=g.get_repo(d['user']+'/'+d['repo'])    
    u=d['other']
    start=T.regex_match_one(u,r'^/tree/[a-z0-9]+/')##==T.regex_match_one(s,r'^\/tree\/[a-z0-9]+\/')
    if not start:
        py.pdb()()
        raise py.ArgumentError(url)
    ############# arg parse ############    
    return_str=U.get_duplicated_kargs(ka,'return_str','rs','return_s',default=return_str)
    return_fullpath=U.get_duplicated_kargs(ka,'return_fullpath','return_full_path','fullpath','path','rp',default=return_fullpath)
    if return_str:return_object=False    
    if not return_fullpath:return_object=False    
    ####################################    
    os=repo.get_dir_contents(u[py.len(start):])    
    if return_object:
        return os
    else:
        if return_fullpath:
            return [o.path for o in os]
        else:
            return [o.name for o in os]
        
github_dir=get_github_dir=get_github_repo_directory_as_list


def github_upload(filename,repo='',commit_msg='',print_requests=False,safe_filename='',token=None,**ka):
    '''
    
- 常规文件
d 目录
b 块类型特殊文件
c 字符类型特殊文件
l 符号链接
p 管道
s 套接字


'/home/qgb/test/fn/\\'
ArgumentError: ('is not bytes',                 ###<py.No|IsADirectoryError(21, 'Is a directory'),'/home/qgb/test/fn//'  2022-06-27__04.10.51__>)
How to fix ? : F.gbAutoPath=0


'/home/klk/test/fn/#'
github_api:  path cannot end with a slash


'''    
    import requests,stat,json
    if not stat.S_ISREG(os.stat(filename).st_mode):return py.No(os.stat(filename),filename,)
    
    if not commit_msg:commit_msg=U.stime()+' '+str(F.size(filename))+filename
    
    print_requests=U.get_duplicated_kargs(ka,'show','print','p','print_req','print_request','print_requests',default=print_requests)
    
    if not repo:repo,token=U.get_or_input('repo,token',default='',type=py.eval)
    # token=U.get_or_input(G+'token',default='')
    token=token.strip()
    if not token.startswith('token '):token='token '+token
    
    # filename=F.auto_path(filename)
    if not safe_filename:
        safe_filename=os.path.basename(filename)
        # if U.isWin():
            # safe_filename=T.path_legalized('/'+F.auto_path(filename),reduce_space=False)[1:]
        # else:    
            # safe_filename=T.path_legalized(F.auto_path(filename),reduce_space=False)
    
    if '/.git/' in safe_filename:
        pass# python pass keyword won't skip execution
        ''' path contains a malformed path component '''
        
    import base64
    s64=base64.b64encode(F.read_bytes(filename)).decode('ascii')
    
    url=f'https://api.github.com:443/repos/{repo}/contents/{T.url_encode(safe_filename)}'
    data='{"message": %s, "content": "%s", "branch": "master"}'%(json.dumps(commit_msg),s64)
    
    
    ka={'headers': {'Authorization': token,
  'User-Agent': 'PyGithub/Python',
  'Content-Type': 'application/json'},
 'timeout': 15,
 'verify': True,
 'allow_redirects': False}
 
    if print_requests:
        print(U.v.requests.put(url,data.encode('utf-8'),**ka) )
    return requests.put(url,data.encode('utf-8'),**ka) 
    #data.encode('utf-8') fix UnicodeEncodeError: 'latin-1' codec can't encoding characters  

upload_github=github_upload    

def github_get_repo(repo,token=GITHUB_TOKEN,**ka):
    '''
    pip install pygithub
    '''
    import github
    token=github_get_token(token,**ka)
    g=github.Github(token)
    return g.get_repo(repo)

def github_get_token(token=GITHUB_TOKEN,**ka):
    '''
    '''
    if not token:
        token=U.get_or_set_input('github.token')
    return token    

def github_get_branch_all_commits(repo,branch,count=90,token=GITHUB_TOKEN,**ka):
    '''count=900 ,耗时5分钟 count=90 耗时 45秒'''    
    repo=github_get_repo(repo,token=token,**ka)
    branch=repo.get_branch(branch)
    pl= repo.get_commits() # <github.PaginatedList.PaginatedList at 0x1ca808150c8> 每页 30 
    rc=[]
    for n,c in enumerate(pl):
        row=c,U.StrRepr(c.raw_data['commit']['message'])
        rc.append(row)

        # print('%-5s'%n,c.sha)
        if (n+1)>=count:break
    return rc    

    return github.Repository.Repository.get_commits()
    return [c for c in branch.get_commits()]
    
GITLAB_TOKEN=py.No('GITLAB_TOKEN')

def gitlab_get_brance_all_commits(repo,branch,count=90,gitlab_url='https://gitlab.com/',token=GITLAB_TOKEN,**ka):
    '''pip install python-gitlab 
    '''
    import gitlab
    gitlab_url=U.get_duplicated_kargs(ka,'gitlab_url','url','u',default=gitlab_url)

    if not token:
        token=U.get_or_set_input(gitlab_url+'.token')
    gl=gitlab.Gitlab(gitlab_url,token)

    return gl
    repo=gl.projects.get(repo)
    branch=repo.branches.get(branch)
    rc=[]
    for n,c in enumerate(branch.commits):
        row=c,U.StrRepr(c.message)
        rc.append(row)
        # print('%-5s'%n,c.sha)
        if (n+1)>=count:break
    return rc    

    return [c for c in branch.get_commits()]    

def gitlab_get_repo_all_branches(repo ):
    return repo.branches.list()

def gitlab_get_all_projects(gitlab_url='https://gitlab.com/',count=None,token=GITLAB_TOKEN,**ka):
    '''pip install python-gitlab 

p.path_with_namespace     
    '''
    import gitlab
    gitlab_url=U.get_duplicated_kargs(ka,'gitlab_url','url','u',default=gitlab_url)

    if not token:
        token=U.get_or_set_input(gitlab_url+'.token')


    gl=gitlab.Gitlab(gitlab_url)

    count_is_int=py.isint(count)
    r=[]
    for n,p in enumerate(gl.projects.list(iterator=True)):
        print( U.stime(),n,p.id,U.StrRepr(p.path_with_namespace,size=60),p.last_activity_at )
        r.append(p)
        if count_is_int and count>0 and (n+1)>=count:break
    return r    
gitlab_get_all_repo=gitlab_get_all_projects    

def clone_specific_commit(u,convert_to_ssh=True,dir_name=py.No('auto repo_name')):
    # ipy=U.get_ipython()
    if convert_to_ssh:
        url=N.git_https_to_ssh(u)
        # 'git@github.com:'
    else:
        raise py.NotImplementedError()
    # for s in u.split('/'):
    cid=T.regex_match_one(u,'[a-f0-9]{40,}')
    
    if not dir_name:
        dir_name=T.sub_last(url,'/','')
        
    repo_path=U.pwd()+dir_name
    if not F.exist(repo_path):
        F.mkdir(repo_path)
    U.cd(repo_path,p=1)    
    U.ipy_system(f'git init')
    U.ipy_system(f'git fetch {url} {cid}')
    U.ipy_system(f'git branch master {cid}')
    U.ipy_system(f'git checkout')
clone_commit=clone_specific_commit