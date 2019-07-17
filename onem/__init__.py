import json

from . import menus, forms


class Response(object):
    def __init__(self, obj, corr_id):
        """
        :param obj: a Menu of Form instance
        :param corr_id: uuid4 string identifier
        """
        assert isinstance(obj, (menus.Menu, forms.Form))

        self.object = obj
        self.corr_id = corr_id

    def as_data(self):
        return {
            'corr_id': self.corr_id,
            'content_type': self.object.as_data()['type'],
            'content': self.object.as_data()
        }

    def as_json(self):
        return json.dumps(self.as_data())
