from .app import App
from .collection import FormSubmissions
from .model import FormSubmission


# @App.path(model=Root, path='/submit/{formname}')
# def get_root():
#     return Root()


# @App.path(model=Document, path='documents/{id}',
#           converters={'id': int})
# def get_document(request, id):
#     return request.db_session.query(Document).filter(Document.id == id).first()


@App.path(model=FormSubmissions, path='/submissions')
def get_document_collection(request, offset=0, limit=10):
    return FormSubmissions(request.db_session, offset, limit)
