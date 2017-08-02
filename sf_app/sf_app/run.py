import sqlalchemy

from webob import static
import morepath

from .app import App, Session
from .model import Base

dirapp = static.DirectoryApp('./rendered')

@App.static_components()
def get_static_components():
  return dirapp

def run():   # pragma: no cover
    engine = sqlalchemy.create_engine('sqlite:///sf_app.db')
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)

    morepath.autoscan()
    morepath.run(App())
