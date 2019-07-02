import json

from onem.common import sanitize_method, sanitize_url


class MenuItem(object):
    def __init__(self, label, url=None, method=None, is_option=True):
        """
        :param label: string used in the item's description
        :param url: the callback url path triggered when accessing this item
        :param method: how the callback url will be triggered
        :param is_option: bool to indicate whether the item is an option item
                          or a separator item. The separator option body are
                          used for presentational purposes only, so url and
                          method won't count here
        """
        self.is_option = is_option

        if not self.is_option:
            self.label = label
            self.url = None
            self.method = None
            return

        self.label = label
        self.url = sanitize_url(url)
        self.method = sanitize_method(method)

    def as_data(self):
        return {
            'description': self.label,
            'method': self.method,
            'path': self.url,
            'type': 'option' if self.is_option else 'content'
        }

    def as_json(self):
        return json.dumps(self.as_data())


class Menu(object):
    def __init__(self, body, header=None, footer=None):
        """
        :param body: sequence of MenuItem instances
        :param header: string displayed in the header
        :param footer: string displayed in the footer
        """
        self.header = header
        self.footer = footer

        assert isinstance(body, (list, tuple))
        for item in body:
            assert isinstance(item, MenuItem)

        self.body = body

    def as_data(self):
        return {
            'type': 'menu',
            'header': self.header,
            'footer': self.footer,
            'body': [item.as_data() for item in self.body]
        }

    def as_json(self):
        return json.dumps(self.as_data())
