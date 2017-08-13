from sys import argv, exit

import sqlalchemy
import morepath

from .app import App, Session
from .model import Base

def config_settings(list_name):
    settings_dict = {'session_info': {'name': list_name}}
    with open('form-data/{}.txt'.format(list_name)) as fd:
        forms = [f.rstrip() for f in fd.readlines()]
        # Check for duplicates
        if len(forms) > len(set(forms)):
            print('You have duplicates in your form list\n' +
                  'This will result in skipping!')
        settings_dict['next_form'] = \
            {k: v for k, v in zip(forms[:-1], forms[1:])}

    # Don't think it matters if this comes before or after autoscan
    # But needs to be before commit(App)
    App.init_settings(settings_dict)
    print(settings_dict)

def run():   # pragma: no cover
    # This is super-hacky, but whatever - this was always intended to be a
    # temporary solution anyway
    if len(argv) > 1:
        # We clean the config filename off so as not to confuse morepath
        config_settings(argv.pop())
    else:
        print('Need a list name (should be in form-data/)')
        exit(1)


    engine = sqlalchemy.create_engine('sqlite:///sf_app.db')
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)

    morepath.autoscan()

    # Not entirely clear if I need this
    morepath.commit(App)
    morepath.run(App())
