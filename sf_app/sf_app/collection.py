from .model import FormSubmission
import json

# MAX_LIMIT = 20


class FormSubmissions(object):
    def __init__(self, db_session, offset, limit):
        self.db_session = db_session
        self.offset = offset
        self.limit = limit  # min(limit, MAX_LIMIT)

    def query(self):
        return self.db_session.query(FormSubmission).offset(self.offset)
            # .limit(self.limit)

    def add(self, session_name, sz_id, form_name, responses):
        '''Add a record to our submissions

        Note that responses will be encoded - it should be sent in as a raw
        python dict / list / etc.'''
        session = self.db_session
        document = FormSubmission(session=session_name, sz_id=sz_id,
                                  form_name=form_name,
                                  responses=json.dumps(responses))
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
