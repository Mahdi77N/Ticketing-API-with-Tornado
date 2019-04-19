import requests
import os
import platform
import time
import sys

PARAMS = CMD = USERNAME = PASSWORD = token = ""
username = password = ""
HOST = "127.0.0.1"
PORT = "1104"
message_id = 0
req = {}

def __authgetcr__():
    return "http://"+HOST+":"+PORT+"/"+CMD+"/"+USERNAME+"/"+PASSWORD


def __postcr__():
    return "http://"+HOST+":"+PORT+"/"+CMD+"?"


def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def show_func():
    print("Username: " + str(USERNAME) + "\n" + "Token: " + str(token))
    print("""What Do You Prefer To Do :
    1. Send ticket
    2. Receive ticket
    3. Change ticket status
    4. Answer to ticket (Just for managers)
    5. Logout
    6. Exit
    """)


while True:
    clear()
    print("""Welcome to ticketing client :)
    Choose what to do:
    1. SignUp
    2. Login
    3. Exit
    """)
    action = sys.stdin.readline()[:-1]
    if action == '1':   # SignUp
        clear()
        while True:
            print("To Create New Account Enter The Authentication")
            print("Username: ")
            USERNAME = sys.stdin.readline()[:-1]
            print("Password: ")
            PASSWORD = sys.stdin.readline()[:-1]
            print("First Name: ")
            fn = sys.stdin.readline()[:-1]
            print("Last Name: ")
            ln = sys.stdin.readline()[:-1]
            CMD = "signup"
            clear()
            PARAMS = {'username': USERNAME, 'password': PASSWORD, 'firstname': fn, 'lastname': ln}
            req = requests.post(__postcr__(), PARAMS).json()
            if str(req['message']) == "Signed Up Successfully":
                print("Your Account Is Created\n" + "Your Username: " + USERNAME + "\nYour token: " + req['token'])
                raw_input('Press enter to continue: ')
                break
            else:
                print("Username exists\nTry again...")
                time.sleep(1)
    if action == '2':  # Login
        clear()
        print("""How to login?
        1. Using token
        2. Using Username & Password
        """)
        login_type = sys.stdin.readline()[:-1]
        if login_type == '1':
            clear()
            while True:
                print("token: ")
                token = sys.stdin.readline()[:-1]
                CMD = "apicheck"
                req = requests.get("http://"+HOST+":"+PORT+"/"+CMD+"/"+token).json()
                if req['message'] == "Signed Up Successfully":
                    clear()
                    print("Token is correct\nLogging you in...")
                    USERNAME = req['username']
                    username = USERNAME
                    PASSWORD = req['password']
                    password = PASSWORD
                    token = req['token']
                    time.sleep(1)
                    break
                else:
                    clear()
                    print("Token is incorrect\nTry again...")
                    time.sleep(1)
        elif login_type == '2':
            clear()
            while True:
                print("Username: ")
                USERNAME = sys.stdin.readline()[:-1]
                username = USERNAME
                print("Password: ")
                PASSWORD = sys.stdin.readline()[:-1]
                password = PASSWORD
                CMD = "login"
                req = requests.get("http://"+HOST+":"+PORT+"/"+CMD+"/"+USERNAME+"/"+PASSWORD).json()
                if req['message'] == "Logged in Successfully":
                    clear()
                    print("Username AND Password is correct\nLogging You in ...")
                    token_db = req['token']
                    token = token_db['token']
                    time.sleep(1)
                    break
                else:
                    clear()
                    print("Username and Password are incorrect\nTry again...")
                    time.sleep(1)
        while True:
            clear()
            show_func()
            func_to_do = sys.stdin.readline()[:-1]
            if func_to_do == '1':   # Send Ticket
                clear()
                CMD = "sendticket"
                print("Subject: ")
                subject = sys.stdin.readline()
                print("Body: ")
                body = sys.stdin.readline()
                PARAMS = {'token': str(token), 'subject': subject, 'body': body}
                # data = requests.get("http://"+HOST+":"+PORT+"/"+CMD+"/"+str(api_token)+"/"+subject+"/"+body)
                data = requests.post(__postcr__(), PARAMS).json()
                print("Your ticket is sent :)")
                raw_input('Press enter to continue: ')
            if func_to_do == '2':   # Get ticket
                clear()
                rule = req['rule']
                if rule == "user":
                    clear()
                    CMD = "getticketcli"
                    data = requests.get("http://"+HOST+":"+PORT+"/"+CMD+"/"+str(token)).json()
                    print("Ticket information:")
                    print(data)
                    raw_input('Press enter to continue: ')
                elif rule == "manager":
                    clear()
                    CMD = "getticketmod"
                    data = requests.get("http://"+HOST+":"+PORT+"/"+CMD+"/"+str(token)).json()
                    print("Ticket information:")
                    print(data)
                    raw_input('Press enter to continue: ')
            if func_to_do == '3':   # Change ticket status
                clear()
                print("""Which one?
                1. Close a Ticket
                2. Open a Ticket
                """)
                work = sys.stdin.readline()[:-1]
                rule = req['rule']
                if work == '1':
                    clear()
                    if rule == "user":
                        CMD = "closeticket"
                        print("Message id: ")
                        message_id = int(sys.stdin.readline())
                        PARAMS = {'token': token, 'id': message_id}
                        data = requests.post(__postcr__(), PARAMS).json()
                        # data = requests.get("http://"+ HOST+":"+PORT+"/"+CMD+"/"+token+"/"+message_id).json()
                        print(data['message'])
                        raw_input('Press enter to continue: ')
                    else:
                        print("Access Denied!")
                        time.sleep(1)
                elif work == '2':
                    if rule == "manager":
                        CMD = "changestatus"
                        token = req['token']
                        print("Status: ")
                        status = sys.stdin.readline()[:-1]
                        PARAMS = {'token': token, 'id': message_id, 'status': status}
                        data = requests.post(__postcr__(), PARAMS)
                        print(data['message'])
                        raw_input('Press enter to continue: ')
                    else:
                        print("Access Denied!")
                        time.sleep(1)
            if func_to_do == '4':   # Answer to ticket
                clear()
                rule = req['rule']
                if rule == "user":
                    CMD = "restoticketmod"
                    print("Body: ")
                    body = sys.stdin.readline()[:-1]
                    print("Message ID: ")
                    message_id = int(sys.stdin.readline())
                    PARAMS = {'token': token, 'id': message_id, 'body': body}
                    data = requests.post(__postcr__(), PARAMS).json()
                    print(data['message'])
                    raw_input('Press enter to continue: ')
                else:
                    print("Access Denied!")
            if func_to_do == '5':   # LogOut
                clear()
                # CMD = "logout"
                # data = requests.get("http://"+HOST+":"+PORT+"/"+CMD+"/"+str(username)+"/"+str(password)).json()
                # if data['message'] == "Logged Out Successfully":
                #   print("Logged Out Successfully")
                #   time.sleep(1)
                print("GoodBye *_*")
                time.sleep(1)
                sys.exit()
                # else:
                #   print("Cannot Log Out:(\nTry again...")
                #   time.sleep(1)
            if func_to_do == '6':   # Exit
                print("GoodBye *_*")
                time.sleep(1)
                sys.exit()
    if action == '3':
        print("GoodBye *_*")
        time.sleep(1)
        sys.exit()
    else:
        print("Wrong Command!")
        time.sleep(1)
