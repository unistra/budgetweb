VERSION = (1, 2, 5)


def get_version():
    return '.'.join(str(num) for num in VERSION[:3])
