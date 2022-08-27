from django.contrib import admin
from .models import Contact, CsvDoc

# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = ["gender", "first_name",
                    "last_name", "date_created", "date_updated"]


class CsvDocAdmin(admin.ModelAdmin):
    list_display = ["file_name"]


admin.site.register(Contact, ContactAdmin)
admin.site.register(CsvDoc, CsvDocAdmin)
