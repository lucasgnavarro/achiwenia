import random


def credentials_generator(length=8):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    pw_length = int(length)
    mypw = ''

    for i in range(pw_length):
        next_index = random.randrange(26)
        mypw += alphabet[next_index]

    return mypw


class TenantManager(object):
    def create_database(self): #TODO
        pass

    def create_db_user(self): #TODO
        pass

    def create_db_password(self): #TODO
        pass

    def check_schema_sync(self): #TODO
        pass

    def sync_database(self): #TODO
        pass
