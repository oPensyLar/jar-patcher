import ssh_class
import wmi
from pypsrp.client import Client

srv_lst = "srv.lst"

# login creds
user = "you-ad-user"
passwd = "you-ad-password"

ssh_port = 22

remote_folder_linux = "/tmp/"

local_file_linux = "log4j_vuln_upgrade.py"
local_file_win = "log4j_vuln_upgrade.ps1"

remote_file_script = remote_folder_linux + local_file_linux
file_name_log = "log4j_vuln_upgrade.log"
remote_file_log = remote_folder_linux + file_name_log

cmd_linux = "python3.7 " + remote_file_script


def deploy_linux(ip_addr, ssh_obj):

    local_script_linux = "P:\\movibles\\PycharmProjects\\log4j-vuln-upgrade\\scripts\\" + local_file_linux
    ssh_obj.sftp_upload_file(local_script_linux, remote_file_script)
    print("[+] Exec py3 script over remote host ...")
    ssh_obj.ssh_cmd(cmd_linux)

    print("[+] Fetching logs on remote host ...")
    local_log_file = "logs/" + ip_addr + ".log"
    ssh_obj.sftp_get_file(local_log_file, remote_file_log)


def deploy_win(ip, usr, pwd):
    with open("C:\\Users\\opensylar\\Desktop\\scripts\\ps1\\log4j_vuln_upgrade.ps1", "r") as fp:
        script_raw = fp.read()

        print("[+] Connecting remote host ...")
        with Client(ip, username=usr, password=pwd, ssl=False) as client:
            print("[+] Exec PS script over remote host ...")
            stdout, stderr, rc = client.execute_ps(script_raw)

            print("[+] Fetching logs on remote host ...")
            local_file_name = "logs\\" + ip + ".log"
            client.fetch("log4j_vuln_upgrade.log", local_file_name)


def deploy():
    with open(srv_lst, "r") as fp:
        for c_srv in fp.readlines():
            c_srv = c_srv.strip('\n').strip('\r').strip('\r\n')

            ssh = ssh_class.SshClient(c_srv, ssh_port, user, passwd)

            if ssh.ssh_cmd("ls -la") is None:
                print("[+]" + c_srv + " is Windows hosts")
                deploy_win(c_srv, user, passwd)

            else:
                print(c_srv + " is Linux hosts")
                deploy_linux(c_srv, ssh)


deploy()