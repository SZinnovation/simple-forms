from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy import register

from more.transaction import TransactionApp
from more.static import StaticApp
from morepath.reify import reify
from morepath.request import Request

Session = sessionmaker()
register(Session)


class DBSessionRequest(Request):

    @reify
    def db_session(self):
        return Session()


class App(StaticApp, TransactionApp):
    request_class = DBSessionRequest
