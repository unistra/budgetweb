VERSION = (1, 2, 10)


def get_version():
    return '.'.join(str(num) for num in VERSION[:3])
