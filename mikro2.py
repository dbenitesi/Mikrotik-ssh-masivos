#!/usr/bin/python

import socket
import sys
import time
import paramiko

def time_stamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def log_filename():
    return time.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"

log_file = log_filename()

# Arte ASCII - Puedes personalizar esto con un generador de arte ASCII online
ascii_art = """
It Danoi
https://danielbenites.com
"""

print(ascii_art)  # Muestra el arte ASCII en la terminal

try:
    f = open("hosts", "r")
except IOError:
    print("\nFile 'hosts' does not exist or is not accessible.\n")
    quit()

nlines = 0
mt_username = "instalador"
mt_password = "nine2022"
timeout = 10

with open(log_file, "a") as log:
    log.write(ascii_art + "\n")  # Escribe el arte ASCII en el archivo de log
    
    for line in f:
        nlines += 1
        host = line.strip()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        message = f"\nConnecting to {nlines}. host: {host}\n"
        print(message)
        log.write(message)
        
        try:
            ssh.connect(host, username=mt_username, password=mt_password, timeout=timeout)
        except socket.timeout:
            message = "Connection timeout.\n"
            print(message)
            log.write(message)
            continue
        except paramiko.AuthenticationException:
            message = "Wrong credentials.\n"
            print(message)
            log.write(message)
            continue
        except Exception as e:
            message = f"Error connecting to the device: {str(e)}.\n"
            print(message)
            log.write(message)
            continue

        message = "Successfully connected to the host. Executing commands:\n"
        print(message)
        log.write(message)
        
        try:
            with open("commands", "r") as k:
                for command in k:
                    command = command.strip()
                    if command:
                        message = f"Executing command: {command}\n"
                        print(message)
                        log.write(message)
                        stdin, stdout, stderr = ssh.exec_command(command)
                        output = "".join(stdout.readlines())
                        print(output)
                        log.write(output + "\n")
                        time.sleep(0.2)
        except IOError:
            message = "\nFile 'commands' does not exist or is not accessible.\n"
            print(message)
            log.write(message)
            continue

        message = "Commands executed successfully.\n"
        print(message)
        log.write(message)
        ssh.close()
    
    if nlines == 0:
        message = "\nList of hosts is empty.\n"
        print(message)
        log.write(message)
f.close()
