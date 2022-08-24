from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name",
                  "gender", "category", "contact_avatar"]

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
        self.fields["last_name"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
        self.fields["category"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
        self.fields["contact_avatar"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
        self.fields["gender"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
