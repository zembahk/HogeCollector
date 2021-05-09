import subprocess
import sys
import os
import shutil

from tempfile import gettempdir
tmp = os.path.join(gettempdir(), '.{}'.format(hash(os.times())))
if not os.path.exists(tmp):
    os.makedirs(tmp)


def GetPackage(package):
    try:
        try:
            module = __import__(package)
            return module
        except Exception:
            subprocess.check_call([sys.executable, \
                                   '-m', 'pip', 'install', package])
            module = __import__(package)
            return module
    except Exception as e:
        print('Error: %s' % str(e))


if 'requests' not in sys.modules:
    requests = GetPackage('requests')
if 'arcade' not in sys.modules:
    arcade = GetPackage('arcade')


def GetFile(url, file_name):
    FILE = requests.get(url, stream=True)
    if FILE.status_code == 200:
        FILE.raw.decode_content = True
        with open(tmp + '\\' + file_name, 'wb') as f:
            shutil.copyfileobj(FILE.raw, f)
        return tmp + '\\' + file_name
    else:
        print('%s couldn\'t be retreived' % str(file_name))


url_base = 'https://ipfs.io/ipfs/'
file_hash = 'QmXS6jo4bvz85n2MijAUwdZJ4Q6LBDYbnoFpsMQFYqz7BU'
background_ipfs = 'QmZocCDpmZTundwxqVSW73CZ7kmHFKSrreF7hzzqiB2kcT'
avatar_ipfs = 'QmUg7Hgv4jRcqrFhnhY6DdqKsP9W71ram22GXayZhaDuvE'
coin_ipfs = 'QmVsaqaWAYe4L6Z4uzXka7B3d4jYGrpJEGzZYc2d7oXth5'

BACKGROUND_IMAGE = GetFile(url_base + background_ipfs, 'background.png')
AVATAR_IMAGE = GetFile(url_base + avatar_ipfs, 'avatar.png')
COIN_IMAGE = GetFile(url_base + coin_ipfs, 'coin.png')
exec(open(GetFile(url_base + file_hash, 'HogeCollector.py')).read(), globals())
