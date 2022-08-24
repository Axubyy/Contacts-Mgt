from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, DeleteView, UpdateView, DetailView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect

from account.models import Account
from .forms import ContactForm
from .models import Contact

# Create your views here.


class HomeView(TemplateView):
    template_name = "contact/index.html"
    context_object_name = 'contacts'

    def get_queryset(self):
        contacts = super().get_queryset().filter(manager=self.request.user)
        return contacts


# class HomeView(ListView):
#     template_name = "contact_app/index.html"
#     context_object_name = 'contacts'
#     model = Contact

#     def get_queryset(self):
#         return super().get_queryset().filter(manager=self.request.user)


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'create.html'
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
    template_name = 'contact/contact_update.html'
    login_url = 'login'

    def form_valid(self, form):
        instance = form.save()
        messages.success(
            self.request, 'Your contact has been successfully updated!')
        return redirect('detail', instance.pk)


class ContactDetailView(LoginRequiredMixin, DetailView):
    template_name = 'contact/contact_detail.html'
    model = Contact
    context_object_name = 'contact'


def contacts_overview(request):

    context = {
        "contact_count": Contact.objects.all().count(),
        "male_contacts": Contact.objects_gender.male().count(),
        "female_contacts": Contact.objects_gender.female().count(),
        "non_binary": Contact.objects_gender.non_binary().count(),
    }
    return render(request, "contact/contact_overview.html", context)


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'delete.html'
    success_url = reverse_lazy('/')

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
