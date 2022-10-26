
from django.db import models
from account.models import Account
from django.urls import reverse

from contact.validators import file_validator

# Create your models here.


class MyAccountContactsGenderManager(models.Manager):
    def female(self):
        return super().get_queryset().filter(gender="F")

    def male(self):
        return super().get_queryset().filter(gender="M")

    def non_binary(self):
        return super().get_queryset().filter(gender="NB")


class MyAccountContactsCategoryManager(models.Manager):
    def family(self):
        return super().get_queryset().filter(category="Family")

    def friends(self):
        return super().get_queryset().filter(category="Friends")

    def work(self):
        return super().get_queryset().filter(category="Work")


class Contact(models.Model):
    CHOICES = (
        ("NB", "Non-Binary"),
        ("M", "Male"),
        ("F", "Female"),
    )
    CATEGORIES = (
        ("FM", "Family"),
        ("WK", "Work"),
        ("FR", "Friends"),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    manager = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="contacts")
    gender = models.CharField(max_length=20, choices=CHOICES, default="M")
    category = models.CharField(
        max_length=20, choices=CATEGORIES, default="Family")
    contact_avatar = models.FileField(
        upload_to="contacts/avatar", default="avatar.png")
    favourite = models.ManyToManyField(
        Account, related_name="favourite", default=None, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    objects_gender = MyAccountContactsGenderManager()
    objects_category = MyAccountContactsCategoryManager()

    def __str__(self) -> str:
        return self.first_name

    def get_absolute_url(self):
        return reverse("contact-detail", kwargs={"pk": self.pk})


class CsvDoc(models.Model):
    file_name = models.FileField(
        upload_to="files/csvs", validators=[file_validator], default=None)
    activated = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f" File id {self.file_name}"
