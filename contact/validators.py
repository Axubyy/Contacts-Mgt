import os
from django.core.exceptions import ValidationError


def file_validator(value):
    extension = os.path.splitext(value.name)[1]
    print(extension)
    valid_extension = ['.csv']
    if not extension in valid_extension:
        raise ValidationError('File extension not allowed. Only' +
                              str(valid_extension))
