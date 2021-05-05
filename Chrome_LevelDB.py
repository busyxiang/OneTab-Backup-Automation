import plyvel
import os

# DONT USE THIS, this is WIP
# Stil cannot figure out why the leveldb is corrupted

USER_PROFILE = os.environ['USERPROFILE']
path = os.path.join(USER_PROFILE, 'AppData', 'Local', 'Google',
                    'Chrome', 'User Data', 'Default', 'Local Extension Settings', 'chphlpgkkbolifaimnlloiipkdnihall_py')
# plyvel.repair_db(path)
# db = plyvel.DB(path, paranoid_checks=True, compression=None)
db = plyvel.DB(path, paranoid_checks=True)

for key, value in db:
    print(key)
    print(value)
