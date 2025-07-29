"""
假设3台电脑，其中：
电脑A，云服务器，具有公网IP182.43.65.44
电脑B，内网电脑，上面的20010端口提供了web服务
电脑C，其余可以连接互联网的电脑

如果需要将电脑B上的服务提供给公网，使得电脑C可以访问，则需要在电脑B上执行如下命令：
ssh -R 0.0.0.0:5000:127.0.0.1:20010 root@182.43.65.44
root@182.43.65.44是用root用户登陆电脑A，并将电脑B的20010端口映射到182.43.65.44的5000端口，如果一切正常，则可以在公网中通过182.43.65.44:5000访问内网提供的服务了。

如果执行后，公网仍不能访问，则需要修改云服务器(即电脑A)中的SSH设置。
vim /etc/ssh/sshd_config

设置以下参数，允许远程端口转发。
GatewayPorts yes

秘钥登陆设置的方法。
 1.首先生成密钥对，在电脑B上执行：
    ssh-keygen
 然后一致回车，知道生成id_isa和id_isa.pub文件

 2.将公钥上传到云服务器A上，分两种情况：
 如果电脑B是windows系统，需要在powershell中执行以下命令：
    type $env:USERPROFILE\.ssh\id_rsa.pub | ssh root@182.43.65.44 "cat >> .ssh/authorized_keys"
 其中，root@182.43.65.44表示root是远程登陆的用户名，182.43.65.44是远程登陆的服务器，即电脑A的ip地址。
 如果电脑B是linux系统，则直接执行以下命令：
    ssh-copy-id -i ~/.ssh/id_rsa.pub root@182.43.65.44
 即可。

如上设置后，可能还需要解决ssh保持活跃的设置


"""
from yangke.core import runCMD


def check_ssh_tunnel_exist(remote_host, remote_port):
    cmd = f"powershell wget https://{remote_host}:{remote_port}"
    msg, err = runCMD(cmd, charset='utf8', timeout=5)
    if "无法连接到远程服务器" in err:
        # 说明端口未进行隧道转发
        return False
    elif "基础连接已经关闭" in err:
        # 说明目标服务使用了https服务，但是SSL证书不安全，但隧道转发是正常的
        return True
    else:
        return True


def ssh_远程转发(remote_ip, remote_port, local_port, login_user):
    """
    该函数需要在提供服务的计算机上执行，一般提供服务的计算机为内网计算机，没有公网ip，该方法将内网计算机上的服务映射到公网ip服务器的端口上。
    Args:
        remote_ip: 远程服务器的ip，一般为租赁的云服务器，具有公网ip
        remote_port: 远程服务器开放的端口
        local_port: 内网计算机提供服务的端口
        login_user: 远程服务器的ssh登录用户名

    Returns:

    """

    cmd = f"ssh -R 0.0.0.0:{remote_port}:127.0.0.1:{local_port} {login_user}@{remote_ip} -o ServerAliveInterval=60 -o ServerAliveCountMax=3"
    if not check_ssh_tunnel_exist(remote_ip, remote_port):  # 如果端口转发不存在
        runCMD(cmd)


if __name__ == "__main__":
    # ssh_远程转发("182.43.65.44", "5000", "20010", "root")
    print(check_ssh_tunnel_exist("101.37.118.81", "20011"))
