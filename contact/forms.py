from dataclasses import field
from django import forms

from .models import Contact, CsvDoc


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name",
                  "gender", "category", "contact_avatar"]

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs["class"] = "mt-1 focus: ring-indigo-500 focus: border-indigo-500 block w-full shadow-sm sm: text-sm border-indigo-300 rounded-md"
        self.fields["last_name"].widget.attrs["class"] = "mt-1 focus: ring-indigo-500 focus: border-indigo-500 block w-full shadow-sm sm: text-sm border-indigo-300 rounded-md"
        self.fields["category"].widget.attrs["class"] = "mt-1 focus: ring-indigo-500 focus: border-indigo-500 block w-full shadow-sm sm: text-sm border-indigo-300 rounded-md"
        self.fields["contact_avatar"].widget.attrs["class"] = "mt-1 focus: ring-indigo-500 focus: border-indigo-500 block w-full shadow-sm sm: text-sm border-indigo-300 rounded-md"
        self.fields["gender"].widget.attrs["class"] = "mt-1 focus: ring-indigo-500 focus: border-indigo-500 block w-full shadow-sm sm: text-sm border-indigo-300 rounded-md"


class CsvForm(forms.ModelForm):
    class Meta:
        model = CsvDoc
        fields = ["file_name", ]

    def __init__(self, *args, **kwargs):
        super(CsvForm, self).__init__(*args, **kwargs)

        self.fields["file_name"].widget.attrs["class"] = "mt-1 focus: ring-indigo-500 focus: border-indigo-500 block w-full shadow-sm sm: text-sm border-indigo-300 rounded-md"

    def clean(self):
        cleaned_data = super(CsvForm, self).clean()
        file_name = cleaned_data.get('file_name')
