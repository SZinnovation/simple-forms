import sqlalchemy
import yaml
import morepath

from .app import App, Session
from .model import Base

def run():   # pragma: no cover
    engine = sqlalchemy.create_engine('sqlite:///sf_app.db')
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)

    # XXX We should get this from argv
    list_name = 'full'
    with open('form-data/{}.txt'.format(list_name)) as fd:
        forms = [f.rstrip() for f in fd.readlines()]
        settings_dict = {'next_form': 
                            {k: v for k, v in zip(forms[:-1], forms[1:])}}

    # Don't think it matters if this comes before or after autoscan
    # But needs to be before commit(App)
    App.init_settings(settings_dict)
    
    morepath.autoscan()
    # Not entirely clear if I need this
    morepath.commit(App)
    morepath.run(App())
