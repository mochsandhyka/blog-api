def User():
    schema = {
        "name" : str,
        "username" : str,
        "password" : str,
        "email" : str
    }
    return schema

def update_user():
    schema = {
        "name" : str,
        "username" : str,
        "password" : str,
        "email" : str,
        "address" : str,
        "rt" : str,
        "rw" : str,
        "kelurahan_desa" : str,
        "kecamatan" : str
    }
    return schema

