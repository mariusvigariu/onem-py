import unittest

from onem.menus import MenuItem, Menu, MenuMeta
from onem import forms


class TestMenu(unittest.TestCase):
    def test_menu_item_option(self):
        item = MenuItem('Some option label',
                        '/callback-path',
                        method='GET',
                        text_search='This is some text attached to some option'
                                    ' label and it is used to help the user '
                                    'narrow down the options when sending '
                                    'something to the platform.')
        expected = {'description': 'Some option label',
                    'method': 'GET',
                    'path': '/callback-path',
                    'type': 'option',
                    'text_search': 'This is some text attached to some option '
                                   'label and it is used to help the user '
                                   'narrow down the options when sending '
                                   'something to the platform.'}

        self.assertEqual(item.as_data(), expected)

    def test_menu_item_content(self):
        item = MenuItem('Get creative with content items', is_option=False)

        expected = {'description': 'Get creative with content items',
                    'method': None,
                    'path': None,
                    'type': 'content',
                    'text_search': None}

        self.assertEqual(item.as_data(), expected)

    def test_menu(self):
        item1 = MenuItem('First menu item', '/callback-1')
        item2 = MenuItem('Second menu item', '/callback-2')
        item3 = MenuItem('Some content here', is_option=False)

        menu = Menu([item1, item2, item3],
                    header='menu header',
                    footer='menu footer',
                    meta=MenuMeta())

        expected = {'type': 'menu',
                    'header': 'menu header',
                    'footer': 'menu footer',
                    'body': [{'description': 'First menu item',
                              'method': 'GET',
                              'path': '/callback-1',
                              'type': 'option',
                              'text_search': None},
                             {'description': 'Second menu item',
                              'method': 'GET',
                              'path': '/callback-2',
                              'type': 'option',
                              'text_search': None},
                             {'description': 'Some content here',
                              'method': None,
                              'path': None,
                              'type': 'content',
                              'text_search': None}],
                    'meta': {'auto_select': True}}

        self.assertEqual(menu.as_data(), expected)


class TestForm(unittest.TestCase):
    def test_string_form_item(self):
        item = forms.StringFormItem(
            'full_name',
            confirmation_label='Chosen name',
            footer='send your name',
            header='name',
            label='Please send your full name',
            method='POST',
            url='/callback-url-triggered-after-name-was-sent',
            validate_url='/callback-url-for-custom-validation',
            min_length=5,  # no names less than 5 chars
            min_length_error='Name is too short. Try again',
            max_length=20,  # no names greater than 20 chars
            max_length_error='Name is too long. Use a shorter one'
        )
        expected = {'name': 'full_name',
                    'type': 'string',
                    'chunking_footer': None,
                    'confirmation_label': 'Chosen name',
                    'editable': True,
                    'footer': 'send your name',
                    'header': 'name',
                    'description': 'Please send your full name',
                    'method': 'POST',
                    'required': True,
                    'status_exclude': False,
                    'status_prepend': False,
                    'url': '/callback-url-triggered-after-name-was-sent',
                    'validation': {
                        'url': '/callback-url-for-custom-validation',
                        'type_error': None,
                        'type_error_footer': None,
                        'min_length': 5,
                        'min_length_error': 'Name is too short. Try again',
                        'max_length': 20,
                        'max_length_error': 'Name is too long. Use a shorter one'}}

        self.assertEqual(item.as_data(), expected)

    def test_hidden_form_item(self):
        item = forms.HiddenFormItem('hidden', 'value given for this item')
        expected = {'name': 'hidden',
                    'type': 'string',
                    'chunking_footer': None,
                    'confirmation_label': None,
                    'editable': True,
                    'footer': None,
                    'header': None,
                    'description': None,
                    'method': None,
                    'required': True,
                    'status_exclude': False,
                    'status_prepend': False,
                    'url': None,
                    'validation': {'url': None, 'type_error': None, 'type_error_footer': None},
                    'hidden': True,
                    'value': 'value given for this item'}
        self.assertEqual(item.as_data(), expected)

    def test_int_form_item(self):
        item = forms.IntFormItem('age',
                                 label='How old are you?',
                                 min_value=12,
                                 min_value_error='You are too young to join our program')

        expected = {'name': 'age',
                    'type': 'int',
                    'chunking_footer': None,
                    'confirmation_label': None,
                    'editable': True,
                    'footer': None,
                    'header': None,
                    'description': 'How old are you?',
                    'method': None,
                    'required': True,
                    'status_exclude': False,
                    'status_prepend': False,
                    'url': None,
                    'validation': {'url': None,
                                   'type_error': None,
                                   'type_error_footer': None,
                                   'min_value': 12,
                                   'min_value_error': 'You are too young to join our program',
                                   'max_value': None,
                                   'max_value_error': None}}

        self.assertEqual(item.as_data(), expected)

    def test_float_form_item(self):
        item = forms.FloatFormItem('ranking',
                                   label='Enter your ranking',
                                   max_value=9.9,
                                   max_value_error='Ranking is too high. Try again.')

        expected = {'name': 'ranking',
                    'type': 'float',
                    'chunking_footer': None,
                    'confirmation_label': None,
                    'editable': True,
                    'footer': None,
                    'header': None,
                    'description': 'Enter your ranking',
                    'method': None,
                    'required': True,
                    'status_exclude': False,
                    'status_prepend': False,
                    'url': None,
                    'validation': {'url': None,
                                   'type_error': None,
                                   'type_error_footer': None,
                                   'min_value': None,
                                   'min_value_error': None,
                                   'max_value': 9.9,
                                   'max_value_error': 'Ranking is too high. Try again.'}}

        self.assertEqual(item.as_data(), expected)

    def test_date_form_item(self):
        item = forms.DateFormItem('scheduled_date',
                                  label='Enter your preferred date')

        expected = {'name': 'scheduled_date',
                    'type': 'date',
                    'chunking_footer': None,
                    'confirmation_label': None,
                    'editable': True,
                    'footer': None,
                    'header': None,
                    'description': 'Enter your preferred date',
                    'method': None,
                    'required': True,
                    'status_exclude': False,
                    'status_prepend': False,
                    'url': None,
                    'validation': {'url': None, 'type_error': None, 'type_error_footer': None}}

        self.assertEqual(item.as_data(), expected)

    def test_datetime_form_item(self):
        item = forms.DateTimeFormItem('scheduled_date',
                                      label='Enter your preferred date')

        expected = {'name': 'scheduled_date',
                    'type': 'datetime',
                    'chunking_footer': None,
                    'confirmation_label': None,
                    'editable': True,
                    'footer': None,
                    'header': None,
                    'description': 'Enter your preferred date',
                    'method': None,
                    'required': True,
                    'status_exclude': False,
                    'status_prepend': False,
                    'url': None,
                    'validation': {'url': None, 'type_error': None, 'type_error_footer': None}}

        self.assertEqual(item.as_data(), expected)

    def test_menu_form_item(self):
        opts = [
            forms.MenuItemFormItem('First option', 'first'),
            forms.MenuItemFormItem('Some content here', is_option=False),
            forms.MenuItemFormItem('Second option', 'second'),
        ]
        item = forms.MenuFormItem('poll', opts,
                                  label='Choose your preferred option',
                                  meta=forms.MenuFormItemMeta(multi_select=True))

        expected = {'name': 'poll',
                    'type': 'form-menu',
                    'chunking_footer': None,
                    'confirmation_label': None,
                    'editable': True,
                    'footer': None,
                    'header': None,
                    'description': 'Choose your preferred option',
                    'method': None,
                    'required': True,
                    'status_exclude': False,
                    'status_prepend': False,
                    'url': None,
                    'validation': {'url': None, 'type_error': None, 'type_error_footer': None},
                    'meta': {'auto_select': False, 'multi_select': True, 'numbered': False},
                    'body': [{'description': 'First option',
                              'type': 'option',
                              'text_search': None,
                              'value': 'first'},
                             {'description': 'Some content here',
                              'type': 'content',
                              'text_search': None,
                              'value': None},
                             {'description': 'Second option',
                              'type': 'option',
                              'text_search': None,
                              'value': 'second'}]}

        self.assertEqual(item.as_data(), expected)

    def test_form(self):
        items = [
            forms.StringFormItem(
                'full_name',
                confirmation_label='Chosen name',
                footer='send your name',
                header='name',
                label='Please send your full name',
                method='POST',
                url='/callback-url-triggered-after-name-was-sent',
                validate_url='/callback-url-for-custom-validation',
                min_length=5,  # no names less than 5 chars
                min_length_error='Name is too short. Try again',
                max_length=20,  # no names greater than 20 chars
                max_length_error='Name is too long. Use a shorter one'
            ),
            forms.HiddenFormItem('hidden', 'value given for this item'),
            forms.IntFormItem('age',
                              label='How old are you?',
                              min_value=12,
                              min_value_error='You are too young to join our program'),
            forms.FloatFormItem('ranking',
                                label='Enter your ranking',
                                max_value=9.9,
                                max_value_error='Ranking is too high. Try again.'),
            forms.DateFormItem('scheduled_date',
                               label='Enter your preferred date'),
        ]

        form = forms.Form(items, '/callback-url-to-post-user-choices-to',
                          method='POST',
                          meta=forms.FormMeta(status=False, confirm=False))

        expected = {'type': 'form',
                    'header': None,
                    'footer': None,
                    'body': [{'name': 'full_name',
                              'type': 'string',
                              'chunking_footer': None,
                              'confirmation_label': 'Chosen name',
                              'editable': True,
                              'footer': 'send your name',
                              'header': 'name',
                              'description': 'Please send your full name',
                              'method': 'POST',
                              'required': True,
                              'status_exclude': False,
                              'status_prepend': False,
                              'url': '/callback-url-triggered-after-name-was-sent',
                              'validation': {'url': '/callback-url-for-custom-validation',
                                             'type_error': None,
                                             'type_error_footer': None,
                                             'min_length': 5,
                                             'min_length_error': 'Name is too short. Try again',
                                             'max_length': 20,
                                             'max_length_error': 'Name is too long. Use a shorter one'}},
                             {'name': 'hidden',
                              'type': 'string',
                              'chunking_footer': None,
                              'confirmation_label': None,
                              'editable': True,
                              'footer': None,
                              'header': None,
                              'description': None,
                              'method': None,
                              'required': True,
                              'status_exclude': False,
                              'status_prepend': False,
                              'url': None,
                              'validation': {'url': None, 'type_error': None, 'type_error_footer': None},
                              'hidden': True,
                              'value': 'value given for this item'},
                             {'name': 'age',
                              'type': 'int',
                              'chunking_footer': None,
                              'confirmation_label': None,
                              'editable': True,
                              'footer': None,
                              'header': None,
                              'description': 'How old are you?',
                              'method': None,
                              'required': True,
                              'status_exclude': False,
                              'status_prepend': False,
                              'url': None,
                              'validation': {'url': None,
                                             'type_error': None,
                                             'type_error_footer': None,
                                             'min_value': 12,
                                             'min_value_error': 'You are too young to join our program',
                                             'max_value': None,
                                             'max_value_error': None}},
                             {'name': 'ranking',
                              'type': 'float',
                              'chunking_footer': None,
                              'confirmation_label': None,
                              'editable': True,
                              'footer': None,
                              'header': None,
                              'description': 'Enter your ranking',
                              'method': None,
                              'required': True,
                              'status_exclude': False,
                              'status_prepend': False,
                              'url': None,
                              'validation': {'url': None,
                                             'type_error': None,
                                             'type_error_footer': None,
                                             'min_value': None,
                                             'min_value_error': None,
                                             'max_value': 9.9,
                                             'max_value_error': 'Ranking is too high. Try again.'}},
                             {'name': 'scheduled_date',
                              'type': 'date',
                              'chunking_footer': None,
                              'confirmation_label': None,
                              'editable': True,
                              'footer': None,
                              'header': None,
                              'description': 'Enter your preferred date',
                              'method': None,
                              'required': True,
                              'status_exclude': False,
                              'status_prepend': False,
                              'url': None,
                              'validation': {'url': None,
                                             'type_error': None,
                                             'type_error_footer': None}}],
                    'meta': {'completion_status_show': False,
                             'completion_status_in_header': True,
                             'confirmation_needed': False},
                    'path': '/callback-url-to-post-user-choices-to',
                    'method': 'POST'}

        self.assertEqual(form.as_data(), expected)


if __name__ == '__main__':
    unittest.main()
