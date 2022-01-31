import ssh_class

# SSH creds
srv_lst = "srv.lst"
port = 22
user = "you-ad-user"
passwd = "you-ad-password"
remote_folder = "/tmp/"
local_file = "log4j_vuln_upgrade.py"
remote_file_script = remote_folder + local_file
file_name_log = "log4j_vuln_upgrade.log"
remote_file_log = remote_folder + file_name_log
cmd = "python3.7 " + remote_file_script


def deploy():
    with open(srv_lst, "r") as fp:
        for c_srv in fp.readlines():
            c_srv = c_srv.strip('\n').strip('\r').strip('\r\n')
            local_log_file = "logs/" + c_srv + ".log"

            ssh = ssh_class.SshClient(c_srv, port, user, passwd)
            ssh.sftp_upload_file(local_file, remote_file_script)
            ssh.ssh_loop(cmd)
            ssh.sftp_get_file(local_log_file, remote_file_log)


deploy()