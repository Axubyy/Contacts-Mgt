from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('detail/<int:pk>/', views.ContactDetailView.as_view(),
         name="contact-detail"),
    path('search/', views.SearchView, name="search"),
    path('contacts/create', views.ContactCreateView.as_view(), name="create-contact"),
    path('contacts/update/<int:pk>',
         views.ContactUpdateView.as_view(), name="update-contact"),
    path('contacts/delete/<int:pk>',
         views.ContactDeleteView.as_view(), name="delete-contact"),
]
