import json

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
        'time': self.time.isoformat(),
        'form_name': self.form_name,
        'submission': json.loads(self.responses),
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
    # In our case, this should just return a dict copy of the underlying
    # webob.MutliDict
    everything = request.POST.mixed()

    # We're going to put these directly in our table, so we also remove from
    # the dict that will be treated as JSON
    form_name = everything.pop('form-name', 'missing')
    sz_id = everything.pop('sz-id', 'missing')

    # While we're using sqlite, I'm just putting the JSON into a string. We
    # should keep it JSON if we switch to postgresql.
    self.add(form_name=form_name, sz_id=sz_id, responses=str(everything))
    # next_form = request.POST.get('next-form')

    # This will probably be an error if form_name was missing
    next_form = getattr(request.app.settings.next_form, form_name)

    # This is a link outside the morepath app, so we just write it directly as
    # a string
    return redirect('{}.html?sz-id={}'.format(next_form, sz_id))
