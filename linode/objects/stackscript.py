from .base import Base, Property
from linode.api import api_call

from enum import Enum

class UserDefinedFieldType(Enum):
    text = 1
    select_one = 2
    select_many = 3

class UserDefinedField():
    def __init__(self, name, label, example, field_type, choices=None):
        self.name = name
        self.label = label
        self.example = example
        self.field_type = field_type
        self.choices = choices

    def __repr__(self):
        return "{}({}): {}".format(self.label, self.field_type.name, self.example)

class StackScript(Base):
    api_endpoint = '/stackscripts/{id}'
    properties = {
        "created": Property(is_datetime=True),
        "label": Property(mutable=True),
        "script": Property(),
        "description": Property(mutable=True),
        "distributions": Property(relationship=True),
        "deployments_total": Property(),
        "is_public": Property(mutable=True),
        "revision_note": Property(),
        "user_defined_fields": Property(),
    }

    def __init__(self, id):
        Base.__init__(self)

        self._set('id', id)

    def _populate(self, json):
        """
        Override the populate method to map user_defined_fields to
        fancy values
        """
        Base._populate(self, json)

        mapped_udfs = []
        for udf in self.user_defined_fields:
            t = UserDefinedFieldType.text
            choices = None
            if hasattr(udf, 'oneof'):
                t = UserDefinedFieldType.select_one
                choices = udf.oneof.split(',')
            elif hasattr(udf, 'manyof'):
                t = UserDefinedFieldType.select_many
                choices = udf.manyof.split(',')

            mapped_udfs.append(UserDefinedField(udf.name, udf.label, udf.example, t, \
                    choices=choices))

        self._set('user_defined_fields', mapped_udfs)
