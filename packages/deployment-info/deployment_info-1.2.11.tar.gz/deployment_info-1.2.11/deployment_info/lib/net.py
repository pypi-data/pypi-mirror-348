import socket


def resolve(pre, idx, id, base):
    v = "%s.%s.%s.%s" % (pre, idx, id, base)
    try:
        socket.gethostbyname(v)
    except Exception as e:
        pass
