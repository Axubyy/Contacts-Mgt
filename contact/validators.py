import os
from django.core.exceptions import ValidationError


def file_validator(value):
    extension = os.path.splitext(value.name)[1]
    # valid_extension = ['jpg', 'jpeg', 'png']
    valid_extension = 'csv'
    if extension != valid_extension:
        raise ValidationError('File extension not allowed. Only' +
                              str(valid_extension))
