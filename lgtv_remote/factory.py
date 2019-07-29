from pywebostv.connection import WebOSClient

from lgtv_remote.exeception import ClientError
from lgtv_remote.settings import SettingsInterface


class WebOSClientFactory:
    def __init__(self, settings: SettingsInterface):
        self.settings = settings

    def create(self, path: str, friendly_name: str) -> WebOSClient:
        self.settings.load(path)
        settings = self.settings.get(friendly_name)
        try:
            host = settings.host
        except KeyError:
            raise ClientError('Missing TV IP address. Please authenticate with your TV.') from None
        try:
            store = {'client_key': settings.client_key}
        except KeyError:
            raise ClientError('Missing client key. Please authenticate with your TV.') from None

        client = WebOSClient(host)
        client.connect()
        status = client.register(store)
        if not all([s == WebOSClient.REGISTERED for s in status]):
            raise ClientError(f'Error connecting to TV {host}. Please authenticate again.')
        return client

    def discover(self):
        devices = WebOSClient.discover()
        for device in devices:
            print(device.host)

    def authenticate(self, friendly_name: str, host: str, path: str):
        settings = self.settings
        store = {}
        friendly_name = friendly_name or host

        client = WebOSClient(host)
        client.connect()
        prompted = False
        for status in client.register(store):
            if status == WebOSClient.PROMPTED:
                prompted = True
        if not prompted:
            raise ClientError(f'Unable to authenticate with TV {host}.')
        if 'client_key' not in store:
            raise ClientError(f'Client key not retrieved from TV {host}.')
        client_key = store['client_key']
        settings.set(friendly_name, host, client_key)
        settings.serialize(path)
