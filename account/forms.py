from django import forms
from .models import Account, UserProfile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Enter your Password",
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm your password"
    }))

    class Meta:
        model = Account
        fields = ["email", "first_name", "last_name",
                  "username", "password", "phone_number"]

        labels = {
            "username": " Your Name",
            "first_name": "Your First Name",
            "last_name": "Your Last name",
            "email": "Your Email Address",
            "phone_number": "Your Phone Number"
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "Enter Your First Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Enter Your Last Name"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Enter Your Phone Number"
        self.fields["email"].widget.attrs["placeholder"] = "Enter Email Address"
        self.fields["password"].widget.attrs["placeholder"] = "Enter Your Password"
        self.fields["confirm_password"].widget.attrs["placeholder"] = "Confirm Your Password"
        # for f
        self.fields["first_name"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
        self.fields["last_name"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
        self.fields["username"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
        self.fields["email"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
        self.fields["password"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
        self.fields["confirm_password"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
        self.fields["phone_number"].widget.attrs["class"] = "mt-1 focus: ring-indigo-500 focus: border-indigo-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(" Password doesn't match!")


class ResetPasswordForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Enter your new password",
        "class": "appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm password",
        "class": "appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
    }))

    class Meta:
        model = Account
        fields = ["password"]


class PasswordChangeForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Enter your Password",
        "class": "appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
    }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Enter your new password",
        "class": "appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm password",
        "class": "appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
    }))

    class Meta:
        model = Account
        fields = ["password"]

    # def __init__(self, *args, **kwargs):
    #     super(UserProfileForm, self).__init__(*args, **kwargs)

    #     self.fields["first_name"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
    #     self.fields["last_name"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
    #     self.fields["username"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
    #     self.fields["email"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
    #     self.fields["profile_pix"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
    #     self.fields["bio"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Enter Your Password"
    }))

    class Meta:
        model = Account
        fields = ["email", "password"]


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["first_name", "last_name", "username", "email"]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs["class"] = "mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm: text-sm border-gray-400 rounded-md"
        self.fields["last_name"].widget.attrs["class"] = "mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm: text-sm border-gray-400 rounded-md"
        self.fields["username"].widget.attrs["class"] = "mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm: text-sm border-gray-400 rounded-md"
        self.fields["email"].widget.attrs["class"] = "mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm: text-sm border-gray-400 rounded-md"


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["profile_pix", "location", "phone_number"]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields["profile_pix"].widget.attrs["class"] = "mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm: text-sm border-gray-400 rounded-md"
        self.fields["location"].widget.attrs["class"] = "mt-1 focus:ring-indigo-500 focus:border-indigo-500  block w-full shadow-sm sm: text-sm border-gray-400 rounded-md"
        self.fields["phone_number"].widget.attrs["class"] = "mt-1 ring-indigo-500 focus:border-indigo-500  block w-full shadow-sm sm: text-sm border-gray-400 rounded-md"
