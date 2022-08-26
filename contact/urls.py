from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('all-contacts/', views.contacts_overview, name='all-contacts'),
    path('detail/<int:pk>/', views.ContactDetailView.as_view(),
         name="contact-detail"),
    path('search/', views.SearchView, name="search"),
    path('create/<int:pk>/', views.ContactCreateView.as_view(),
         name="create-contact"),
    path('update/<int:pk>/',
         views.ContactUpdateView.as_view(), name="update-contact"),
    path('delete/<int:pk>/',
         views.ContactDeleteView.as_view(), name="delete-contact"),
    path('fav/<int:contact_pk>/', views.add_contact_as_favourite, name="favourite"),
    path('favourites/', views.list_favourites_contacts, name='favourite-contacts'),
    path('export-csv/<int:account_pk>/',
         views.generate_contact_csv, name='export-contacts'),
    path('import-csv/<int:account_pk>/',
         views.import_csv, name="import-contacts")
]
