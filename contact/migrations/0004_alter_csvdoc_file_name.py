# Generated by Django 4.1 on 2022-08-26 00:57

import contact.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_rename_csvdocs_csvdoc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvdoc',
            name='file_name',
            field=models.FileField(upload_to='files/csvs', validators=[contact.validators.file_validator]),
        ),
    ]
