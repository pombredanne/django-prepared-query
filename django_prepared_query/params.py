import random
from django.db.models import Expression


class BindParam(Expression):
    def __init__(self, name, field_type=None):
        super(BindParam, self).__init__(None)
        self.name = name
        self.field_type = field_type
        if self.field_type:
            self.field_type.validators = []  # Disable validation for user specified field types
            if not self.field_type.max_length:
                self.field_type.max_length = 256
        self.hash = '%032x' % random.getrandbits(128)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.name)

    def as_sql(self, compiler, connection):
        return '{}', [self.hash]

    def resolve_expression(self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False):
        c = super(BindParam, self).resolve_expression(query, allow_joins, reuse, summarize, for_save)
        query.add_prepare_param(self)
        return c

    def get_group_by_cols(self):
        return []
