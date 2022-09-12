from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, CreateView, DetailView, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.shortcuts import redirect, render, get_object_or_404, HttpResponse


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from .utils import send_email_verification, send_password_reset_verification


from .forms import LoginForm, RegistrationForm, ResetPasswordForm, UserProfileForm, UserForm, PasswordChangeForm
from .models import Account, UserProfile

# # Create your views here.


def register(request):
    print(request.user)
    print('HHHHH')
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        print(form.errors)
        print(form.is_valid())
        if form.is_valid():
            print("Got here too")
            username = form.cleaned_data["username"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]

            print("Got here")
            user = Account.objects.create_user(
                username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.phone_number = phone_number
            user.save()
            send_email_verification(request, user)
            print("Got Here")
            return redirect('/account/login/?command=verification&email=' + email)
        else:

            form = RegistrationForm()
        return render(request, "account/signup.html", {
            "form": form})
    else:
        form = RegistrationForm()
        return render(request, "account/signup.html", {
            "form": form})


@login_required(login_url="login")
def user_profile(request, account_username):
    # user_profile = get_object_or_404(UserProfile, pk=pk)
    user_profile = UserProfile.objects.get(user__username=account_username)

    return render(request, "account/profile.html", {
        "user_profile": user_profile,
    })


def user_login(request):
    print(request.user)
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        print(email, password)
        user = auth.authenticate(email=email, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You have successfully logged-in!")
            return redirect('home')
        else:

            messages.error(request, "Invalid Login Credentials")
    return render(request, 'account/login.html', {
        "form": LoginForm()
    })


@login_required(login_url="login")
def user_logout(request):
    auth.logout(request)
    messages.error(request, "You Just Logged-out!")
    return redirect("login")


def activate(request, uidb64, token):
    try:
        user_pk = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=user_pk)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, "Congratulations! Your account is activated.")
        return redirect('login')

    else:
        messages.error(request, "Invalid Activation Link!")
        return redirect('register')


def forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]

        # user = auth.authenticate(email=email)
        if Account.objects.filter(email__iexact=email).exists():
            user = Account.objects.get(email__iexact=email)
            if user is not None:
                send_password_reset_verification(request, user)
                messages.success(
                    request, "Password reset email has  been sent to email address")
                return redirect('login')
            else:
                messages.error(request, "Invalid User Credential")
                return redirect('forgot-password')

    return render(request, "account/forgot_password.html")

# checks the token and uid from the email sent  and saves the user_pk in the session
# Runs only when the email link is clicked


def reset_password_validate(request, uidb64, token):

    try:
        user_pk = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=user_pk)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = user_pk  # the uid used to get user_pk
        messages.success(request, "Please reset your password")
        return redirect("reset-password")
    else:
        messages.error(request, "This Link has been expired")
        return redirect('forgot-password')


def reset_password(request):

    if request.method == "POST":
        old_password = request.POST["old_password"]
        password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            user_pk = request.session.get("uid")
            user = Account.objects.get(pk=user_pk)
            if user:
                user.set_password(password)  # hashes the password
                user.is_active = True
                user.save()
                messages.success(
                    request,  "Password Reset Successful,Please login with your new password")
                return redirect('login')
        else:
            messages.error(
                request, "Passwords doesn't match. Please Input again")
            return redirect('reset-password')
    else:
        form = ResetPasswordForm()
        return render(request, "account/reset_password.html", {
            "form": form
        })


@login_required(login_url='login')
def change_password(request):
    if request.method == "POST":
        old_password = request.POST["old_password"]
        password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]

        if request.user.check_password(old_password) and password == confirm_password:
            request.user.set_password(password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Your password was updated successfully")
            print("Changed password Here")
            return redirect('change-password')
    else:
        form = PasswordChangeForm()
        return render(request, "account/change_password.html", {
            "form": form
        })


@login_required(login_url='login')
def edit_profile(request, profile_pk):
    print("Here profile")
    if request.method == "POST":
        print("Here profile")
        if UserProfile.objects.filter(pk=profile_pk).exists():
            user_profile = UserProfile.objects.get(pk=profile_pk)
            user_form = UserForm(request.POST,
                                 instance=request.user)
            profile_form = UserProfileForm(
                request.POST, request.FILES, instance=user_profile)

            if user_form.is_valid() and profile_form.is_valid():
                print("Did it")
                user_form.save()
                profile_form.save()
                messages.success(request, "Your Update was saved successfully")
                print("Here")
                return redirect(reverse('edit-profile', args=[profile_pk]))

    else:

        user_form = UserForm(instance=request.user.profile)
        profile_form = UserProfileForm(instance=request.user.profile)
    context = {
        "user_form": user_form,
        "profile_form": profile_form
    }

    return render(request, "account/profile_update.html", context)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    template_name = "account/profile_update.html"
    form_class = UserProfileForm
    context_object_name = 'profile'
    model = UserProfile
    queryset = UserProfile.objects.all()

    def get_success_url(self) -> str:
        return reverse('profile-detail', kwargs={"pk": self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        current_user = self.request.user
        context = super().get_context_data(**kwargs)
        context["user_profile_form"] = UserProfileForm(instance=current_user.profile, initial={
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "username": current_user.username,
            'phone_number': current_user.phone_number,
            "email": current_user.email,
        })

        return context

    def form_valid(self, form: UserProfileForm) -> HttpResponse:
        user_profile = form.save(commit=False)
        print(user_profile)
        user = user_profile.user
        user.first_name = form.cleaned_data.get("first_name")
        user.last_name = form.cleaned_data.get("last_name")
        user.username = form.cleaned_data.get("username")
        user.email = form.cleaned_data.get("email")
        user.phone_number = form.cleaned_data.get("phone_number")
        user.save()
        user_profile.save()
        print("Got here")
        return HttpResponseRedirect(reverse('profile-detail', kwargs={"pk": self.kwargs.get('pk')}))

        # super().form_valid(form)


class ProfileDetailView(DetailView):
    template_name = "account/profile_detail.html"
    context_object_name = 'profile'
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = self.get_object()
        account = account.user
        context["favourite_contacts"] = account.favourite.all()
        return context


# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)
#             messages.success(
#                 request, 'Your password was successfully updated!')
#             return redirect('change_password')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'accounts/change_password.html', {
#         'form': form
#     })


@login_required(login_url='login')
def dashboard(request):
    return render(request, "account/dashboard.html")


def page_404(request, exception=None):
    return render(request, "account/404.html")


def page_403(request, exception=None):
    return render(request, "account/test2.html")


def page_400(request, exception=None):
    return render(request, "account/404.html")


def page_500(request, exception=None):
    return render(request, "account/404.html")
