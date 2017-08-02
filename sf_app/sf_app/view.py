from morepath import redirect

from .app import App
from .collection import FormSubmissions
from .model import FormSubmission


# @App.json(model=Root)
# def root_default(self, request):
#     return redirect('/documents')


@App.json(model=FormSubmission)
def document_default(self, request):
    return {
        'form_name': self.form_name,
        'submission': self.responses,
        # This could be useful, but for now we're not linking to individuals
        # 'link': request.link(self)
    }


@App.json(model=FormSubmissions)
def submissions_default(self, request):
    return {
        'records': [request.view(rec) for rec in self.query()],
        'previous': request.link(self.previous(), default=None),
        'next': request.link(self.next(), default=None),
        # 'add': request.link(self, 'add'),
    }


# We don't currently have a direct form for this... it's static and served by nginx
# @App.html(model=FormSubmissions, name='add')
# def document_collection_add(self, request):
#     return '''\
# <html>
# <body>
# <form action="/documents/add_submit" method="POST">
# title: <input type="text" name="title"><br>
# content: <input type="text" name="content"><br>
# <input type="submit" value="Add!"><br>
# </form>
# </body>
# </html>
# '''


@App.view(model=FormSubmissions, request_method='POST')
def document_collection_add_submit(self, request):
    form_name = request.POST.get('form-name')
    # In our case,  this should just return a dict copy
    everything = request.POST.mixed()
    # While we're prototyping, I'm just putting the JSON into a string. We
    # should keep it JSON in the "real" system.
    record = self.add(form_name=form_name, responses=str(everything))
    return redirect('/thanks.html')
