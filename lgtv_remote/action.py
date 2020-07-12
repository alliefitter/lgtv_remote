import json
from argparse import Action

from lgtv_remote.exeception import ClientError


class JsonInputAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        data = None
        if values:
            try:
                data = json.loads(values)
            except ValueError:
                raise ClientError('Invalid JSON input.') from None
        setattr(namespace, self.dest, data)