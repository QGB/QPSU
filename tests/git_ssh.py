#!/usr/bin/env python3

''' pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn ecdsa cryptography
!C:\QGB\miniforge3\python.exe C:\QGB\miniforge3\Lib\site-packages\pythonwin\qgb\tests\git_ssh.py 

GIT_SSH_COMMAND="ssh -i ~/.ssh/NIST256p.pem" git clone git@ssh.github.com:QGB/


'''
import os,sys,subprocess,ecdsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

def generate_deterministic_keys(secexp, curve='NIST256p', comment="", out_dir=os.path.expanduser('~/.ssh')):
    """
    根据唯一整数 secexp 确定性地生成 ECDSA 私钥并写入 SSH 目录
    """
    # 确保 ~/.ssh 目录存在并设置 700 权限
    os.makedirs(out_dir, mode=0o700, exist_ok=True)
    os.chmod(out_dir, 0o700)
    if curve != "NIST256p":raise ValueError("#TODO 仅支持 NIST256p(secp256r1)")
    if isinstance(secexp, str):
        comment = secexp if not comment else comment
        secexp = int(secexp)
    if not comment:
        comment = str(secexp)
    # 1. 由 secret_exponent 生成 ecdsa 密钥
    sk_ecdsa = ecdsa.SigningKey.from_secret_exponent(secexp=secexp, curve=ecdsa.NIST256p)
    vk_ecdsa = sk_ecdsa.verifying_key
    # 2. 转换为 cryptography 标准 EC 私钥对象
    private_numbers = ec.EllipticCurvePrivateNumbers(
        private_value=secexp,
        public_numbers=ec.EllipticCurvePublicNumbers(
            x=vk_ecdsa.pubkey.point.x(),
            y=vk_ecdsa.pubkey.point.y(),
            curve=ec.SECP256R1()
        )
    )
    priv_key = private_numbers.private_key()
    # 3. 【核心修复】强制导出为 OpenSSH 原生格式 (-----BEGIN OPENSSH PRIVATE KEY-----)
    # 这彻底解决了 ssh 报 "invalid format" 的兼容性问题
    ssh_sk_pem = priv_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.OpenSSH,
        encryption_algorithm=serialization.NoEncryption()
    )
    ssh_priv_path = os.path.join(out_dir, "NIST256p.pem")
    
    # 4. 彻底清洗 \r 回车 (等效于 sed -i 's/\r//g')，并确保严格以 \n 结尾
    clean_pem = ssh_sk_pem.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
    if not clean_pem.endswith(b'\n'):
        clean_pem += b'\n'
    # 使用 "wb" 二进制模式写入，杜绝系统自带换行符干扰
    with open(ssh_priv_path, "wb") as f:
        f.write(clean_pem)
    # 5. 权限加固 (chmod 600)
    os.chmod(ssh_priv_path, 0o600)
    print(f"[+] 私钥已保存并设置 600 权限 (OpenSSH 原生格式): {ssh_priv_path}")
    return ssh_priv_path

def run_ssh_connect(key_path, target="git@ssh.github.com"):
    """
    通过 subprocess 执行 SSH 测试，自动接受 Host Key Fingerprint
    """
    # StrictHostKeyChecking=accept-new 自动同意并记录新的主机指纹
    cmd = [
        "ssh",
        "-i", key_path,
        "-o", "StrictHostKeyChecking=accept-new",
        #"-v",
        target
    ]
    
    print(f"[+] 正在执行 SSH 连接: {' '.join(cmd)}\n")
    # 直接将 SSH 输出打印至标准终端
    subprocess.run(cmd)

if __name__ == "__main__":
    expr = sys.argv[1]
    secexp_val = eval(expr)
    pem_file = generate_deterministic_keys(secexp=secexp_val)
    # 2. 自动发起 SSH 测试
    run_ssh_connect(pem_file, "git@ssh.github.com")
