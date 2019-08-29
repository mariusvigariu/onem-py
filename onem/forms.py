import json

from onem import menus
from onem.common import sanitize_method, sanitize_url


class FormItemType(object):
    STRING = 'string'
    INT = 'int'
    FLOAT = 'float'
    DATE = 'date'
    DATETIME = 'datetime'
    MENU = 'form-menu'


class BaseFormItem(object):
    item_type = None

    def __init__(self, name,
                 chunking_footer=None,
                 confirmation_label=None,
                 editable=True,
                 footer=None,
                 header=None,
                 label=None,
                 method=None,
                 required=True,
                 status_exclude=False,
                 status_prepend=False,
                 url=None,
                 validate_url=None,
                 validate_type_error=None,
                 validate_type_error_footer=None):
        """
        :param name: string used to identify the item
        :param chunking_footer: string displayed in the footer when sms chunks are available
        :param confirmation_label: label of the item shown in the confirmation menu
        :param editable: bool indicating whether this step is editable or not
        :param footer: string used to display in footer for this form item (overwrites Form.footer)
        :param header: string used to display in header for this form item (overwrites Form.header)
        :param label: string used in the item's description
        :param method: how the callback url will be triggered
        :param required: bool indicating whether this item is required or not if set to False this step can be ``SKIP``ed
        :param status_exclude: if True this step will be excluded from the form completion status
        :param status_prepend: if True this step will be prepended to the body pre of the response - appended otherwise
        :param url: the callback url path triggered after a choice has been set on this form item
        :param validate_url: the callback url path (GET) triggered to validate user input
            with query string ?user_input=somesome
            url must return json content {'valid': True/False, 'error': 'Some validation error message'}
        :param validate_type_error: an error message to be shown on basic type validation
        :param validate_type_error_footer: a string displayed in the error message footer
        """
        allowed_item_types = [v for k, v in FormItemType.__dict__.items()
                              if k == k.upper()]

        if self.item_type not in allowed_item_types:
            raise Exception(f'Invalid type. Allowed: {allowed_item_types}')

        self.name = name

        self.chunking_footer = chunking_footer
        self.confirmation_label = confirmation_label
        self.editable = editable
        self.footer = footer
        self.header = header
        self.label = label
        self.required = required
        self.status_exclude = status_exclude
        self.status_prepend = status_prepend
        self.validate_type_error = validate_type_error
        self.validate_type_error_footer = validate_type_error_footer

        if url is not None:
            self.url = sanitize_url(url)
            self.method = sanitize_method(method)
        else:
            self.url = None
            self.method = None

        self.validate_url = sanitize_url(validate_url)

    def as_data(self):
        return {
            'name': self.name,
            'type': self.item_type,
            'chunking_footer': self.chunking_footer,
            'confirmation_label': self.confirmation_label,
            'editable': self.editable,
            'footer': self.footer,
            'header': self.header,
            'description': self.label,
            'method': self.method,
            'required': self.required,
            'status_exclude': self.status_exclude,
            'status_prepend': self.status_prepend,
            'url': self.url,
            'validation': {
                'url': self.validate_url,
                'type_error': self.validate_type_error,
                'type_error_footer': self.validate_type_error_footer,
            },
        }

    def as_json(self):
        return json.dumps(self.as_data())


class StringFormItem(BaseFormItem):
    item_type = FormItemType.STRING

    def __init__(self, name,
                 min_length=None, max_length=None,
                 min_length_error=None, max_length_error=None, **kws):

        super(StringFormItem, self).__init__(name, **kws)

        self.min_length = min_length
        self.min_length_error = min_length_error

        self.max_length = max_length
        self.max_length_error = max_length_error

    def as_data(self):
        data = super(StringFormItem, self).as_data()

        data['validation'].update({
            'min_length': self.min_length,
            'min_length_error': self.min_length_error,
            'max_length': self.max_length,
            'max_length_error': self.max_length_error,
        })

        return data


class HiddenFormItem(BaseFormItem):
    item_type = FormItemType.STRING

    def __init__(self, name, value):

        super(HiddenFormItem, self).__init__(name)

        self.value = value

    def as_data(self):
        data = super(HiddenFormItem, self).as_data()
        data.update({
            'hidden': True,
            'value': self.value,
        })
        return data


class IntFormItem(BaseFormItem):
    item_type = FormItemType.INT

    def __init__(self, name,
                 min_value=None, max_value=None,
                 min_value_error=None, max_value_error=None, **kws):

        super(IntFormItem, self).__init__(name, **kws)

        self.min_value = min_value
        self.min_value_error = min_value_error

        self.max_value = max_value
        self.max_value_error = max_value_error

    def as_data(self):
        data = super(IntFormItem, self).as_data()

        data['validation'].update({
            'min_value': self.min_value,
            'min_value_error': self.min_value_error,
            'max_value': self.max_value,
            'max_value_error': self.max_value_error,
        })

        return data


class FloatFormItem(IntFormItem):
    item_type = FormItemType.FLOAT


class DateFormItem(BaseFormItem):
    item_type = FormItemType.DATE


class DateTimeFormItem(BaseFormItem):
    item_type = FormItemType.DATETIME


class MenuItemFormItem(menus.MenuItem):
    def __init__(self, label, value=None, text_search=None, is_option=True):
        super(MenuItemFormItem, self).__init__(label, text_search=text_search,
                                               is_option=is_option)
        if is_option:
            assert value is not None

        self.value = value

    def as_data(self):
        data = super(MenuItemFormItem, self).as_data()

        data['value'] = self.value

        data.pop('method')
        data.pop('path')

        return data


class MenuFormItemMeta(menus.MenuMeta):
    """ Meta information for a MenuFormItem object """
    def __init__(self, auto_select=False, multi_select=False, numbered=False):
        """
        :param auto_select: if true auto selects the option if the menu
            has only one option
        :param multi_select: allow multiple options to be selected
        :param numbered: display numbers instead of letter option markers
        """
        super(MenuFormItemMeta, self).__init__(auto_select=auto_select)

        for k in (multi_select, numbered):
            assert(isinstance(k, bool))

        self.multi_select = multi_select
        self.numbered = numbered

    def as_data(self):
        data = super(MenuFormItemMeta, self).as_data()
        data.update({
            'multi_select': self.multi_select,
            'numbered': self.numbered,
        })
        return data


class MenuFormItem(BaseFormItem):
    item_type = FormItemType.MENU

    def __init__(self, name, body, meta=None, **kws):
        super(MenuFormItem, self).__init__(name, **kws)

        self.body = body
        for item in body:
            assert isinstance(item, MenuItemFormItem)

        self.meta = meta
        if self.meta is None:
            return

        assert isinstance(self.meta, MenuFormItemMeta)

    def as_data(self):
        data = super(MenuFormItem, self).as_data()
        data['meta'] = self.meta.as_data() if self.meta else None
        data['body'] = [item.as_data() for item in self.body]
        return data


class FormMeta(object):
    """ Meta information for a Form object """
    def __init__(self, status=True, status_in_header=True, confirm=True):
        """
        :param status: boolean whether to show the completion status
        :param status_in_header: boolean whether to show the status in header
                                 or body
        :param confirm: boolean whether the form needs confirmation or not
        """
        self.status = status
        self.status_in_header = status_in_header
        self.confirm = confirm

    def as_data(self):
        return {
            'completion_status_show': self.status,
            'completion_status_in_header': self.status_in_header,
            'confirmation_needed': self.confirm
        }


class Form(object):
    def __init__(self, items, url, header=None, footer=None, method=None,
                 meta=None):
        """
        :param header: string displayed in the header
                       (overwritten by FormItem.header if not None)
        :param footer: string displayed in the footer
                       (overwritten by FormItem.footer if not None)
        :param items: sequence of FormItem instances
        :param url: callback url path triggered after form is finished
        :param method: http method how to callback url will be triggered
        :param meta: FormMeta instance
        """
        self.header = header
        self.footer = footer
        self.items = items

        self.url = sanitize_url(url)
        self.method = sanitize_method(method)

        assert isinstance(items, (list, tuple))
        for item in items:
            assert isinstance(item, BaseFormItem)

        self.meta = meta

        if self.meta is None:
            return

        assert isinstance(self.meta, FormMeta)

    def as_data(self):
        return {
            'type': 'form',
            'header': self.header,
            'footer': self.footer,
            'body': [item.as_data() for item in self.items],
            'meta': self.meta.as_data() if self.meta else None,
            'path': self.url,
            'method': self.method
        }

    def as_json(self):
        return json.dumps(self.as_data())
