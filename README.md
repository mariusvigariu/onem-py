# ONEm python client
Client which defines the JSON structure accepted by ONEm platform.


## Quickstart

ONEm client works only with Python 3. You can use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io) to create a virtual environment.

On a linux box:

```mkvirtualenv --python=`which python3` onem-py```

Then install the ONEm client

`pip install onem-py`


### Menu

```
In [1]: from onem import menus                                                                                                                                          

In [2]: menu_item1 = menus.MenuItem('First menu item', '/callback-path-m1')                                                                                             

In [3]: menu_item2 = menus.MenuItem('Second menu item which is just content', is_option=False)                                                                          

In [4]: menu = menus.Menu([menu_item1, menu_item2],
                          header='Menu header',
                          footer='Displayed at the bottom')

In [5]: menu.as_data()                                                                                                                                                  
Out[5]: 
{'type': 'menu',
 'header': 'Menu header',
 'footer': 'Displayed at the bottom',
 'body': [{'description': 'First menu item',
   'method': 'GET',
   'path': '/callback-path-m1',
   'type': 'option'},
  {'description': 'Second menu item which is just content',
   'method': None,
   'path': None,
   'type': 'content'}],
 'meta': None}

```


### Form

```
In [1]: from onem import forms                                                                                                                                          

In [2]: form_item1 = forms.FormItem('age', forms.FormItemType.INT, 'How old are you?')                                                                                  
In [3]: form_item2 = forms.FormItemMenu('is_number', [ 
   ...:     forms.FormItemMenuItem('Age is just a number, right?', is_option=False), 
   ...:     forms.FormItemMenuItem('Yes!', value=True), 
   ...:     forms.FormItemMenuItem('Not really ...', value=False), 
   ...: ])                                                                                                                                                              

In [4]: form = forms.Form([form_item1, form_item2], 
   ...:                   '/form-callback-path-with-user-choices', 
   ...:                   method='POST', 
   ...:                   header='Form header', 
   ...:                   footer='Form footer', 
   ...:                   meta=forms.FormMeta(confirm=False))                                                                                                           

In [5]: form.as_data()                                                                                                                                                  
Out[5]: 
{'type': 'form',
 'header': 'Form header',
 'footer': 'Form footer',
 'body': [{'description': 'How old are you?',
   'footer': None,
   'header': None,
   'method': None,
   'name': 'age',
   'path': None,
   'type': 'int'},
  {'type': 'form-menu',
   'header': None,
   'footer': None,
   'body': [{'description': 'Age is just a number, right?',
     'type': 'content',
     'value': None},
    {'description': 'Yes!', 'type': 'option', 'value': True},
    {'description': 'Not really ...', 'type': 'option', 'value': False}],
   'meta': None,
   'name': 'is_number'}],
 'meta': {'completion_status_show': True,
  'completion_status_in_header': True,
  'confirmation_needed': False},
 'path': '/form-callback-path-with-user-choices',
 'method': 'POST'}

```
