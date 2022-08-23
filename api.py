from loguru import logger
from configparser import ConfigParser
import conv

import hashlib
import base64

servers = conv.getservers()

cfg = ConfigParser()
cfg.read("config.ini")
SIGN_KEY = cfg['Durak']['sign_key']


def send1command(sock, comm, arg, argcont):
    mrequest = conv.marshal(
        {
            arg: argcont,
            "command": comm
        }
    )
    sock.sendall(mrequest.encode())
    logger.debug(mrequest)


def getsessionkey(sock):
    keyRequest = conv.marshal(
        {
            "v": "1.9.8",
            "l": "ru",
            "n": "durak.android",
            "tz": "+03:00",
            "p": 14,
            "and": 25,
            "d": "samsung zxc",
            "pl": "android",
            "command": "c"
        }
    )
    sock.sendall(keyRequest.encode())
    logger.debug(keyRequest)
    data = sock.recv(4096).decode()
    logger.debug(data)
    key = conv.unmarshal(data)[0]["key"]
    return key


def verifysession(sock, key):
    # проще говоря, ключ с солью SIGN_KEY хешируется md5, а затем хеш переводится в base64. Ничего сложного.
    verifData = base64.b64encode(hashlib.md5((key + SIGN_KEY).encode()).digest()).decode()
    send1command(sock, "sign", "hash", verifData)
    data = sock.recv(4096).decode()
    logger.debug(data)
    data2 = sock.recv(4096).decode()
    logger.debug(data2)


def auth(sock, token):
    send1command(sock, "auth", "token", token)
    for _ in range(2):
        data = sock.recv(4096)
        try:
            logger.debug(data.decode())
        except UnicodeDecodeError:
            logger.debug(data)


def creategame(sock):
    createRequest = conv.marshal(
        {
            "password": 1337,
            "fast": False,
            "ch": False,
            "nb": True,
            "bet": 100,
            "players": 2,
            "sw": False,
            "deck": 36,
            "command": "create"
        }
    )
    sock.sendall(createRequest.encode())
    logger.debug(createRequest)
    for _ in range(2):
        data = sock.recv(4096).decode()
        logger.debug(data)
