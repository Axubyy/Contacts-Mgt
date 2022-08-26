import account
from account.models import UserProfile
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


def profile_info(request):
    print(request.user.first_name, "Okrrr")
    print(request.user.is_authenticated)
    account_profile = None
    if request.user.is_authenticated:
        try:
            account_profile = UserProfile.objects.filter(
                pk=request.user.pk)
            print(account_profile, "Here")
            print(type(account_profile))
        except Exception as e:
            print(e)
            if account_profile is not None:
                return dict(account_profile_pk=account_profile.pk)
            else:
                pass
