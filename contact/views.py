
import csv
from urllib import response
from django.shortcuts import render, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView, DeleteView, UpdateView, DetailView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect


from account.models import Account
from .forms import ContactForm, CsvForm
from .models import Contact, CsvDoc

# Create your views here.


class HomeView(ListView):
    template_name = "contact/index.html"
    context_object_name = 'contacts'
    model = Contact

    def get_queryset(self):
        contacts = super().get_queryset().filter(manager=self.request.user)
        print(contacts)
        return contacts


def home(request):
    if request.user.is_authenticated:
        context = {
            "all_contact": Contact.objects.all().count(),
            "male_contacts": Contact.objects_gender.male().count(),
            "female_contacts": Contact.objects_gender.female().count(),
            "non_binary": Contact.objects_gender.non_binary().count(),
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
        "all_contact": Contact.objects.all().count(),
        "male_contacts": Contact.objects_gender.male().count(),
        "female_contacts": Contact.objects_gender.female().count(),
        "non_binary": Contact.objects_gender.non_binary().count(),
        "all_contacts": Contact.objects.all(),
        "personal_contacts_count": Contact.objects.filter(manager=request.user).count(),
        "personal_contacts": Contact.objects.filter(manager=request.user),
    }
    return render(request, "contact/contacts_overview.html", context)


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'delete.html'
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request, 'Your contact has been successfully deleted!')
        return super().delete(self, request, *args, **kwargs)


# class SignUpView(CreateView):
#     form_class = UserCreationForm
#     template_name = 'registration/signup.html'
#     success_url = reverse_lazy('home')


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
    return HttpResponseRedirect(request.META["HTTP_REFERRER"])


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
        data = request.FILES.get("file_name", None)
        print(data)
        print(form.is_valid())
        print(form.errors)
        print("Formmm")
        if form.is_valid():
            print("here")
            form.save()
            form = CsvForm()
            contact_list = []
            try:
                obj = CsvDoc.objects.get(activated=False)
                with open(obj.file_name.path, 'r') as file:
                    reader = csv.reader(file)
                    for i, row in enumerate(reader):
                        if i == 0:
                            pass
                        else:
                            row = "".join(row)
                            row = row.replace(";", " ")
                            row = row.split()
                            manager = Account.objects.get(username=row[2])

                            import_account = Account.objects.get(pk=account_pk)
                            contact_list.append(Contact(first_name=row[0], last_name=row[1], manager=manager.username,
                                                        gender=row[3], category=row[4], contact_avatar=row[5], favourite=manager.username, date_created=row[7], date_updated=row[8]))
                contacts = Contact.objects.bulk_create(
                    contact_list)
                obj.activated = True
                obj.save()
                messages.success(
                    request, "Your Contact Imports sUccessfully Created!🎉")
            except (TypeError, ValueError, OverflowError, Account.DoesNotExist) as e:
                print(e)

            return redirect('all-contacts')
        else:
            form = CsvForm(request.POST, request.FILES)
            print("else")
            return render(request, "contact/import_csv_form.html", {
                'form': form,
            })
    else:
        form = CsvForm()
        return render(request, "contact/import_csv_form.html", {
            'form': form,
        })
