def User():
    schema = {
        "name" : str,
        "username" : str,
        "password" : str,
        "email" : str
    }
    return schema

def Address():
    schema = {
        "address" : str,
        "rt" : str,
        "rw" : str,
        "kelurahan_desa" : str,
        "kecamatan" : str
    }
    return schema
