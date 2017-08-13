from sys import argv, exit
import sqlalchemy
import morepath

from .app import App, Session
from .model import Base

def run():   # pragma: no cover
    # This is super-hacky, but whatever - this was always intended to be a
    # temporary solution anyway
    if len(argv) > 1:
        # We clean this off so as not to confuse morepath
        list_name = argv.pop()
    else:
        print('Need a list name (should be in form-data/)')
        exit(1)

    with open('form-data/{}.txt'.format(list_name)) as fd:
        forms = [f.rstrip() for f in fd.readlines()]
        settings_dict = {'next_form': 
                            {k: v for k, v in zip(forms[:-1], forms[1:])}}

    # Don't think it matters if this comes before or after autoscan
    # But needs to be before commit(App)
    App.init_settings(settings_dict)

    engine = sqlalchemy.create_engine('sqlite:///sf_app.db')
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)

    morepath.autoscan()
    # Not entirely clear if I need this
    morepath.commit(App)
    morepath.run(App())
