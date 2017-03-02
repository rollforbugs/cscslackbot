Plugin Architecture
===================
The plugin architecture of the CSC Slack bot is very simple. As of right now, a
plugin receives Slack RTM events as the bot receives them, and it can choose to
do with them whatever it desires. In the future, additional bot capabilities
may be added.

Installation
------------
To install a plugin, you need to do two things:
  1. Install the plugin into the directory specified by `plugin_dir` in
     `config.py`.
  2. Add the name of the plugin to the `plugins` list in `config.py`.

Development
-----------
Developing a plugin is fairly simple. You basically just need to add
```python
from cscslackbot.plugins import Plugin
```
to the `__init__.py` of a new module and write a class that subclasses `Plugin`.
Note that `Plugin` itself may be subclassed into templates, for example the
`Command` class also provided in the `cscslackbot.plugins` package.

The basic structure of a plugin looks like this:
```python
from cscslackbot.plugins import Plugin


class AwesomePlugin(Plugin):
    name = 'awesome'
    help_text = 'Does awesome things!'
    help_para = '''Expanded information on why this is awesome.
You can go into quite a bit of detail here if you'd like.
Try to keep help_text short.'''

    def process_event(self, event):
        # Check the type of the message
        if event['type'] != 'message':
            return
        
        # Do something AWESOME with the message!
        pass
```

Note the four attributes on the class:

---

`name`: A short and unique name for the plugin.

This is a required attribute for **ALL** plugins.

The name should match the name of the module you're developing the plugin in.
If it doesn't, the configuration system will break as it is currently written.

_If the name is not present, the system will **not** register the plugin at all,
but it will be possible to use the class you made as a template.  In fact, this
is currently the distinction between plugins and templates, in the way that I'm
referring to them._

---

`help_text`: _optional_ A short description of what the plugin does.

This is referenced by the `help` plugin. I probably should have called this
`description`, but that's not the case. I might change that at some point.

---

`help_para`: _optional_ A longer description of the plugin's functionality.

This is what the `help` plugin displays when you ask for the help for a
specific plugin, and should be much more detailed than the short description.

---

`process_event`: _optional_ A function to call for every event sent by Slack.

This is the main entry point into your plugin as far as the bot is concerned
right now. While there may be more entry points in the future, this is the only
one the bot references as of this writing.

If you have this function defined, the bot will call it every time it receives
an event from the RTM API. It is up to you to check the message type and do
something with the event if you so desire.

---

To build a correct plugin, you need to specify both a `name` and a
`process_event` function for your class, and ideally you should add help.

Templates
---------
If you develop a class that extends `Plugin` but do not define a `name`
attribute, then congratulations! You have developed a template!

Templates are simply skeletons for plugins to make it easier to develop
multiple plugins with similar functionality. If you want to make a custom
template, you can simply design a Python module that creates the class and
drop it into the plugins folder or somewhere within as you would with a
normal plugin. Then, when you create plugins based off of that template, you
can use relative package names to import your template, like
```python
from ..awesometemplate import AwesomeTemplate

class AwesomePlugin(AwesomeTemplate):
    name = 'awesome'
    .
    .
    .
```

There is one template built into the system already, which is the `Command`
template. The `Command` template provides a `process_event` function that
will check that it receives a message with a special prefix (! by default)
and the name of your command, then pass the remainder of that message through
to a `process_command` function that you define if the condition is met.

If you want to add a simple command to the bot, you can do it like this:
```python
from cscslackbot.plugins import Command

class AwesomeCommand(Command):
    name = 'awesome'
    help_text = 'Does awesome things!'
    help_para = '''Expanded information on why this is awesome.
You can go into quite a bit of detail here if you'd like.
Try to keep help_text short.'''
    command = 'ohyeah'

    def process_command(self, event, args):
        # Obey your Slack member overlords
        pass
```

Because the Command template has defined `process_event`, you don't need to do
anything for that!
In fact, _you shouldn't do anything for that unless you want to break the reason
the template even exists in the first place_.
The only new things to you here are these:

---

`command`: _optional_ The command to respond to.

If the prefix is configured as '!' and `command` is 'banana', `process_command`
will be called only when a message is sent that starts with '!banana'.

_If this attribute is not defined, the name will be used as the command by
default._

---

`process_command`: A function to call every time the command is sent.

This is given the original `event` object as well as an `args` object that is
the part of the message string after the command. You don't need to validate
whether the command was called or if the event had a `text` field.

This is **not** optional for a command, simply because the entire purpose of
the `Command` template is to make this a thing.

---

Configuration
-------------
If your plugin relies on configuration values, you should make sure that you
give it a whole folder for its Python module (placing its code in __init__.py).
Inside that folder, you can then create a `defaults.yml` file and fill it in
with an appropriate set of defaults.

This should be a standard YAML file and you can find a bunch of examples of
YAML syntax online. However, it is largely the same as JSON, with a bunch of
additional options available, including comments. To be safe, I would recommend
writing your configuration files as if they were simply JSON.

If a user wants to override a value in your configuration, they only need to
create a dictionary in the global `config.yml` with the name of your plugin and
override the default values there.

For example, your `defaults.yml` for `AwesomePlugin` might look like this:
```yaml
# I'm a comment!
integer_value: 42
float_value: 2.12
string_value: test string
another_string: 'i have quotes'
boolean_value: true
dict_value:
  key1: value1
  key2: value2
  nested_dict:
    key3: value3
dict_but_like_json: {
  'key1': 'value1',
  'key2': 'value2',
  'nested_dict': {
    'key3': 'value3'
  }
}
list_value: [
  item1,
  item2,
]
another_list:
- item1
- - subitem1 # First - creates a list item, second starts the sublist
  - subitem2
- item2
```
and the `config.yml` file might contain the following to override `list_value`
and `integer_value`:
```yaml
# Other config options here
awesome: {
  integer_value: 57,
  list_value: [item3, item4],
}
```

Note how you do _not_ specify the section in your `defaults.yml`. That is
handled by the plugin system automatically for you.

The plugin system will also automatically give your plugin direct access to its
section through the `ClassName.config` / `self.config` attribute.
However, this will only work after the class is defined (and therefore loaded),
which makes it great for use in `process_event` or similar, but perhaps not so
much in setup code.

You can access the global config (and/or secrets) if you really need to by using
```python
from cscslackbot.config import config, secrets
```
Your config would then be available as
```python
config['awesome'] # where 'awesome' is your plugin's name
```
