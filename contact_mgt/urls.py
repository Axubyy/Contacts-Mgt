"""contact_mgt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls import (handler400, handler404, handler403, handler500)

handler500 = "account.views.page_500"
handler403 = "account.views.page_403"
handler404 = "account.views.page_404"
handler400 = "account.views.page_400"
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", RedirectView.as_view(url='contact/')),
    path('contact/', include('contact.urls')),
    path('account/', include("account.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]


# style = "background: linear-gradient(90deg, hsla(217, 100%, 50%, 1) 0%, hsla(186, 100%, 69%, 1) 100%);"
