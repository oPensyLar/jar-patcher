import paramiko
import time
from socket import gaierror


class SshClient:
    host = None
    port = None
    user = None
    password = None
    sftp = None
    transport = None

    def __init__(self, hst, prt, usr, pwd):
        self.host = hst
        self.port = prt
        self.user = usr
        self.password = pwd

    def connect(self):
        self.transport = paramiko.Transport(self.host, self.port)
        self.transport.connect(username=self.user, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def sftp_get_file(self, local_file, remote_file):
        self.connect()
        self.sftp.get(remote_file, local_file)

    def sftp_upload_file(self, local_file, remote_file):
        self.connect()
        self.sftp.put(local_file, remote_file)
        self.sftp.close()
        self.transport.close()

    def ssh_loop(self, cmd):
        repeat = True

        while repeat:
            client = paramiko.client.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.load_system_host_keys()
            time.sleep(1)

            try:
                client.connect(self.host, port=self.port, username=self.user, password=self.password)

            except gaierror:
                print("[!] gaierror")
                continue

            except ConnectionError:
                print("[!] ConnectionError")
                continue

            except TimeoutError:
                print("[!] TimeoutError")
                continue

            except EOFError:
                print("[!] ERROR")
                continue

            except paramiko.ssh_exception.AuthenticationException:
                print("[!] ERROR")
                continue

            except paramiko.ssh_exception.NoValidConnectionsError:
                print("[!] ERROR")
                continue

            try:
                stdin, stdout, stderr = client.exec_command(cmd)

            except ConnectionResetError:
                print("[!] exec_command() ERROR")
                continue

            except paramiko.ssh_exception.SSHException:
                print("[!] SSHException ERROR")
                continue

            stdout = stdout.readlines()
            stderr = stderr.readlines()
            # stdin = stdin.readlines()
            client.close()

            # print(stdin)

            str_output = ''.join(str(e) for e in stdout)
            str_err_output = ''.join(str(e) for e in stderr)
            print()

            return {"stdout": str_output, "stderr": str_err_output}

            # print(stdout)
            # print(stderr)
            repeat = False