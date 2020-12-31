'''
# ---------------------------------------------
# GetRemo v1.1
# Date: 30-12-2020
# Created By: Mahesan G
# ---------------------------------------------
This script running based on paramiko module
This script scans a csv file and execute commands remotely and 
stores the output as result.txt with the script folder 
-----------------------------------------------
create a csv file as input.csv within the script foler like the below format:
hostname,remote_user,user_pass,private_key,commands
<host ip or FQDN >,<remote_user>,<user_pass>,<ssh_key>,<commands>
(EX):
teset.com,ec2-user,/home/user/privatekey.pem,whoami,cat /etc/hosts,uptime
'''


import paramiko
import sys
import csv
from datetime import datetime

class RemoteSSHExecute:
    def __init__(self,rhost,ruser,passwd=None,pkeypath=None,port=22,timeout=10,auth_timeout=10):
        try:
            if not any ([passwd, pkeypath]):
                raise ValueError("Kindly provide either password or SSH key..!!! ")
                sys.exit()
            else:
                self.rhost = rhost
                self.ruser = ruser
                self.passwd = passwd
                self.pkeypath = pkeypath
                self.port = port
                self.auth_timeout = timeout
                self.timeout = auth_timeout
                self.client = None
                self.ssh_out = None
                self.ssh_err = None
        except Exception as e:
            print(f"ERROR: {e}")

    def ssh_connect(self):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if not self.passwd:
                pk = paramiko.RSAKey.from_private_key(open(self.pkeypath))
                self.ssh.connect(hostname=self.rhost,username=self.ruser,pkey=pk,port=self.port,auth_timeout=self.auth_timeout,timeout=self.timeout)
                print("Connected with PrivateKey")
            else:
                self.ssh.connect(hostname=self.rhost,username=self.ruser,password=self.passwd,port=self.port,auth_timeout=self.auth_timeout,timeout=self.timeout)
                print("Connect with Password")
        except paramiko.AuthenticationException:
            print("Authentication Failed, Check Your Credentials")
            result = False
        except paramiko.SSHException as shherr:
            print(f"Could Not Establish SSH connection: {ssherr}")
            result = False
        except Exception as e:
            print(f"ERROR: {e}")
            result = False
            self.ssh.close()
        else:
            result = True
        return result

    def result_to_file(self):
        try:
            if self.result_list:
                ctime = datetime.now()
                current_time = ctime.strftime("%d-%m-%Y-%H%M%S")
                extension = ".txt"
                filename = str(f'Results-{current_time}{extension}')
                with open(filename, 'w') as file:
                    for r in self.result_list:
                        file.write(r)
                self.result_list.clear()
            else:    
                print("No output to write")
        except Exception as e:
            print(f"ERROR WRITEING RESULTS: {e}")

    def command_exec(self,commands):
        self.ssh_out = None
        try:
            if self.ssh_connect():
                self.result_list = []
                start = (f"---------------------------{self.rhost }-------------------------------\n") 
                print(start)
                self.result_list.append(start)               
                for command in commands:
                    stdin, stdout, stderr = self.ssh.exec_command(command,timeout=10)
                    self.std_out = stdout.readlines()
                    self.std_err = stderr.readlines()
                    if self.std_out:
                        list = self.std_out
                    else:
                        list = self.std_err
                    output = (''.join([line.rstrip() for line in list]))   
                    
                    if self.std_err:
                        final_err = (f"Command Failed: {command} \nError:\n{output}\n")
                        print(final_err)
                        self.result_list.append(final_err)
                    else:
                        final_out = (f"Command Executed: {command}\nOutput:\n{output}\n")
                        print(final_out)
                        self.result_list.append(final_out)
                self.result_to_file()
            else:
                print("Unable To Establish SSH Connection")
                self.ssh.close()

        except Exception as e:
            print(f"ERROR: {e}")
            self.ssh.close()
        return None
  

def main():
    try:
        with open('input.csv','r') as csv_file:
            data = csv.DictReader(csv_file)
            for row in data:
                remote_host = row['hostname']
                remote_user = row['remote_user']
                remote_userpass = row['user_pass']
                remote_privatekey = row['private_key']
                commands_raw = row['commands']
                sshclient = RemoteSSHExecute(rhost=remote_host,ruser=remote_user,passwd=remote_userpass,pkeypath=remote_privatekey)
                commands = list(commands_raw.split(",")) 
                sshclient.command_exec(commands=commands)
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()