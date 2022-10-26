
import csv
from django.shortcuts import render, get_object_or_404, HttpResponse, HttpResponseRedirect, redirect
from django.views import View
from django.views.generic import TemplateView, DeleteView, UpdateView, DetailView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse


from account.models import Account
from .forms import ContactForm, CsvForm
from .models import Contact, CsvDoc

# Create your views here.


class HomeView(ListView):
    template_name = "contact/index.html"
    context_object_name = 'contacts'
    model = Contact

    def get_queryset(self):
        print(self.request.user.profile)
        contacts = super().get_queryset().filter(manager=self.request.user)
        print(contacts)
        return contacts


def home(request):
    print(request.user)
    if request.user.is_authenticated:
        context = {
            "all_contact": Contact.objects.all().count(),
            "male_contacts": Contact.objects_gender.male().filter(manager=request.user).count(),
            "female_contacts": Contact.objects_gender.female().filter(manager=request.user).count(),
            "non_binary": Contact.objects_gender.non_binary().filter(manager=request.user).count(),
            "family_count": Contact.objects_category.family().filter(manager=request.user).count(),
            "friends_count": Contact.objects_category.friends().filter(manager=request.user).count(),
            "work_count": Contact.objects_category.work().filter(manager=request.user).count(),
            "family": Contact.objects_category.family().filter(manager=request.user),
            "friends": Contact.objects_category.friends().filter(manager=request.user),
            "work": Contact.objects_category.work().filter(manager=request.user),
            "all_contacts": Contact.objects.all(),
            "personal_contacts_count": Contact.objects.filter(manager=request.user).count(),
            "personal_contacts": Contact.objects.filter(manager=request.user),
        }
        return render(request, "contact/index.html", context)
    else:
        context = {
            "personal_contacts": "Welcome"
        }
    return render(request, "contact/home.html", context)


# class HomeView(ListView):
#     template_name = "contact_app/index.html"
#     context_object_name = 'contacts'
#     model = Contact

#     def get_queryset(self):
#         return super().get_queryset().filter(manager=self.request.user)


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact/create_contact.html'
    # fields = ['first_name', 'email', 'phone', 'info', 'gender', 'image']

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.manager = self.request.user
        instance.save()
        messages.success(
            self.request, 'Your contact has been successfully created!')
        return redirect('home')


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ContactForm
    model = Contact
    template_name = 'contact/contact_update.html'
    login_url = 'login'

    def form_valid(self, form):
        instance = form.save()
        messages.success(
            self.request, 'Your contact has been successfully updated!')
        return redirect('contact-detail', args=[instance.pk])


class ContactDetailView(LoginRequiredMixin, DetailView):
    template_name = 'contact/contact_detail.html'
    model = Contact
    context_object_name = 'contact'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)


def contacts_overview(request):

    context = {
        "all_contact_count": Contact.objects.all().count(),
        "male_contacts": Contact.objects_gender.male().count(),
        "female_contacts": Contact.objects_gender.female().count(),
        "non_binary": Contact.objects_gender.non_binary().count(),
        "family_count": Contact.objects_category.family().filter(manager=request.user).count(),
        "friends_count": Contact.objects_category.friends().filter(manager=request.user).count(),
        "work_count": Contact.objects_category.work().filter(manager=request.user).count(),
        "family": Contact.objects_category.family().filter(manager=request.user),
        "friends": Contact.objects_category.friends().filter(manager=request.user),
        "work": Contact.objects_category.work().filter(manager=request.user),
        "all_contacts": Contact.objects.all(),
        "personal_contacts_count": Contact.objects.filter(manager=request.user).count(),
        "personal_contacts": Contact.objects.filter(manager=request.user),
    }
    return render(request, "contact/contacts_overview.html", context)


# class ContactDeleteView(LoginRequiredMixin, View):
#     def get(self, request, pk, *args, **kwargs):
#         if request.is_ajax():
#             contact = Contact.objects.filter(pk=pk)
#             contact.delete()
#             return JsonResponse({"message":"success"})
#         return JsonResponse({"message": "success"})
class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'delete.html'
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request, 'Your contact has been successfully deleted!')
        return super().delete(self, request, *args, **kwargs)


@login_required(login_url='login')
def SearchView(request):
    if request.method == 'POST':
        kerko = request.POST.get('search')
        print(kerko)
        results = Contact.objects.filter(first_name__contains=kerko)
        context = {
            'results': results
        }
        return render(request, 'users/search_result.html', context)


@login_required(login_url='login')
def list_favourites_contacts(request):
    user_id = request.user
    contacts = Contact.objects.filter(favourite=user_id)
    print(contacts)
    print(user_id.username)
    return render(request, "contact/favourite_contacts.html", {
        "contacts": contacts
    })


@login_required(login_url='login')
def add_contact_as_favourite(request, contact_pk):
    fav = False
    contact = get_object_or_404(Contact, pk=contact_pk)

    if contact.favourite.filter(id=request.user.id).exists():
        fav = False
        contact.favourite.remove(request.user)
        contact.save()

    else:
        contact.favourite.add(request.user)
        contact.save()
        fav = True
        context = {
            "fav": fav,
            "contact": contact
        }
    # return JsonResponse(resp, content_type="application/json")
    return redirect(request.META["HTTP_REFERER"])


def generate_contact_csv(request, account_pk):
    manager = Account.objects.get(pk=account_pk)
    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = 'attachment; filename=contacts.csv'
    # contacts = Contact.objects.all()
    contacts = Contact.objects.filter(manager__pk=account_pk)
    headers = ["first_name", "last_name", "manager", "gender", "category",
               "contact_avatar", "favourite", "date_created", "date_updated"]
    writer = csv.writer(resp)
    writer.writerow(headers)
    for contact in contacts:
        query = contact.favourite.filter(pk=account_pk)
        for attr in query:
            query = attr.username
            print(query)
        writer.writerow([contact.first_name, contact.last_name, contact.manager.username, contact.gender, contact.category,
                        contact.contact_avatar.path, query, contact.date_created, contact.date_updated])
    return resp


def import_csv(request, account_pk):

    if request.method == "POST":
        form = CsvForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            print("here")
            form.save()
            form = CsvForm()
            contact_list = []
            try:
                obj = CsvDoc.objects.get(activated=False)
                print(obj)
                with open(obj.file_name.path, 'r') as file:
                    reader = csv.reader(file)
                    for i, row in enumerate(reader):
                        if i == 0:
                            pass
                        else:
                            print(row[1])
                            import_account = Account.objects.get(pk=account_pk)
                            contact_list.append(Contact(first_name=row[0], last_name=row[1], manager=import_account,
                                                        gender=row[3], category=row[4], contact_avatar=row[5], date_created=row[7], date_updated=row[8]))
                            print(contact_list)
                contacts = Contact.objects.bulk_create(
                    contact_list)
                print("GGG")
                print(contacts)
                print(contact_list)
                obj.activated = True
                obj.save()
                messages.success(
                    request, "Your new Contacts import were successfully Created!🎉")
            except (TypeError, ValueError, OverflowError, Account.DoesNotExist) as e:
                print(e)

            return redirect('all-contacts')
        else:
            print(form.errors)
            messages.error(
                request, "Contacts import error")
            form = CsvForm(request.POST, request.FILES)
            return render(request, "contact/import_csv_form.html", {
                'form': form,
            })
    else:
        form = CsvForm()
        return render(request, "contact/import_csv_form.html", {
            'form': form,
        })
