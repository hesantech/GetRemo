# GetRemo v1.1
Its running based on paramiko module
GetRemo scans a csv file with remote ip, user, password and multiple commands and 
stores the executed commands output as result.txt with the script folder 

# Requirements
```py
$ pip install paramiko
```
# STEPS!
```sh
$ git clone https://github.com/mahesandev/GetRemo.git
```
  - Jus clone and make changes in csv file as per your requirements
#                           OR
  - Directly create a csv file follows the below format:
    hostname,remote_user,user_pass,private_key,commands
  - host ip or FQDN,remote_user,user_pass,ssh_key,commands
  - (EX):
   test.test.org,ec2-user,/home/user/privatekey.pem,whoami,cat /etc/hosts,uptime

# Run as follows:
```py
$ python GetRemo.py
```
- If passoword provided in the csv file script wont check for ssh key
- If you want to use ssh key as authentication type leave the password field blank
- To make it simple I'm not parsing timeout values from csv file if you want to change the timeout value feel free to modify the code as you wish
- All commands are only seperated my , (commas), to seperate commands use ; (semicolon) 

License
----

GNU General Public License v3.0
