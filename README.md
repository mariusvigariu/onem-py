# ONEm python client
Client which defines the JSON structure accepted by ONEm platform.


## Quickstart

ONEm client works only with Python 3. You can use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io) to create a virtual environment.

On a linux box:

```mkvirtualenv --python=`which python3` onem-py```

Then install the ONEm client

`pip install onem-py`


### Menu

Define a menu:

```
from onem import menus

menu_item1 = menus.MenuItem('Say hello', '/hello')
menu_item2 = menus.MenuItem('This is just a separator', is_option=False)

body = (menu_item1, menu_item2)

menu = menus.Menu(body)

print(menu.as_data())

# {'type': 'menu',
#  'header': None,
#  'footer': None,
#  'body': [{'description': 'Say hello',
#    'method': 'GET',
#    'nextRoute': '/hello',
#    'type': 'option'},
#   {'description': 'This is just a separator',
#    'method': None,
#    'nextRoute': None,
#    'type': 'content'}]}

```

Notes:

1. Header and footer are not mandatory and not final. ONEm platform will modify them according to the service standards.


### Form

```
from onem import forms

form_item1 = forms.FormItem('How old are you?', 'age', forms.FormItemType.INT)
form_item2 = forms.FormItem('Age is just a number, right?',
                            'is_number',
                            forms.FormItemType.STRING,
                            header='Just a number',
                            footer='Reply your answer',
                            url='/item-callback-path',
                            method='POST')

body = (form_item1, form_item2)

form = forms.Form(body, '/form-callback-path', header='Form header',
                  method='POST',
                  meta=forms.FormMeta(confirm=False))

print(form.as_data())

# {'type': 'form',
#  'header': 'Form header',
#  'footer': None,
#  'body': [{'description': 'How old are you?',
#    'footer': None,
#    'header': None,
#    'method': None,
#    'name': 'age',
#    'nextRoute': None,
#    'type': 'int'},
#   {'description': 'Age is just a number, right?',
#    'footer': 'Reply your answer',
#    'header': 'Just a number',
#    'method': 'POST',
#    'name': 'is_number',
#    'nextRoute': '/item-callback-path',
#    'type': 'string'}],
#  'meta': {'completion_status_show': True,
#   'completion_status_in_header': True,
#   'confirmation_needed': False},
#  'nextRoute': '/form-callback-path',
#  'method': 'POST'}

```


NOTES: 

1. The header or footer of a `FormItem` will overwrite the header or footer of the `Form`.
2. If present, the `FormItem.url` is triggered immediately after it's been set.
3. `Form.url` is always triggered after all items have been processed.
