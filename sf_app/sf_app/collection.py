from .model import FormSubmission

# MAX_LIMIT = 20


class FormSubmissions(object):
    def __init__(self, db_session, offset, limit):
        self.db_session = db_session
        self.offset = offset
        self.limit = limit  # min(limit, MAX_LIMIT)

    def query(self):
        return self.db_session.query(FormSubmission).offset(self.offset)
            # .limit(self.limit)

    def add(self, form_name, responses):
        session = self.db_session
        document = FormSubmission(form_name=form_name, responses=responses)
        session.add(document)
        session.flush()
        return document

    def previous(self):
        if self.offset == 0:
            return None
        new_offset = max(self.offset - self.limit, 0)
        return FormSubmissions(self.db_session, new_offset, self.limit)

    def next(self):
        count = self.db_session.query(FormSubmission.id).count()
        new_offset = self.offset + self.limit
        if new_offset >= count:
            return None
        return FormSubmissions(self.db_session, new_offset, self.limit)
