VERSION = (2, 4, 2)


def get_version():
    return '.'.join(str(num) for num in VERSION[:3])
