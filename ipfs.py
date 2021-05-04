import ipfshttpclient


# Share TCP connections until the client session is closed
class SomeObject:
    def __init__(self):
        self._client = ipfshttpclient.connect(session=True)

    def do_something(self):
        hash = self._client.add('hoge_coin.png')['ipfs://QmSZAxML86Q9WqEPz7xSM5pdb1VLdMECAzynmnhw14rfKR']
        print(self._client.stat(hash))

    def close(self):  # Call this when your done
        self._client.close()


def main():
    sObject = SomeObject()
    sObject.do_something()
    sObject.close()

if __name__ == "__main__":
    main()
