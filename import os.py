import os
import requests
import shutil

from tempfile import gettempdir
tmp = os.path.join(gettempdir(), '.{}'.format(hash(os.times())))
os.makedirs(tmp)


def GetImage(url, file_name):
    IMAGE = requests.get(url, stream=True)
    if IMAGE.status_code == 200:
        # Set decode_content value to True
        # Otherwise the downloaded image file's size will be zero.
        IMAGE.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(tmp + '\\' + file_name, 'wb') as f:
            shutil.copyfileobj(IMAGE.raw, f)

        return tmp + '\\' + file_name
    else:
        print(file_name + ' couldn\'t be retreived')


url_base = 'https://ipfs.io/ipfs/'
background_ipfs = 'QmdqUB643miPcNTswnT8M8ZzqqEZWqE6JnBmfrmMerRqWr'
avatar_ipfs = 'QmQyLXMHejPPFyXvYi3sZRtPHN2BkEEyUcaFPeoVhZiy7T'
coin_ipfs = 'QmSZAxML86Q9WqEPz7xSM5pdb1VLdMECAzynmnhw14rfKR'

BACKGROUND_IMAGE = GetImage(url_base + background_ipfs, 'background.png')
AVATAR_IMAGE = GetImage(url_base + avatar_ipfs, 'avatar.png')
COIN_IMAGE = GetImage(url_base + coin_ipfs, 'coin.png')

print(tmp)