import string
import socket
import os
import secrets


def generate_secret_key(length):

    password = ''.join(secrets.choice(
        (string.ascii_letters + string.digits)) for i in range(length))
    return password


def generate_instance_id():

    return f"{os.getpid()}__{socket.gethostname().replace('.', '')}"