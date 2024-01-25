
from django.urls import path
from .views import MailingListView, MailingListDetailView, MailingListCreateView, MailingListUpdateView, \
    MailingListDeleteView, HomeView, ClientCreateView, ClientListView, ClientUpdateView, ClientDeleteView, \
    ClientDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('mailinglists/', MailingListView.as_view(), name='mailinglist-list'),
    path('mailinglists/<int:pk>/', MailingListDetailView.as_view(), name='mailinglist-detail'),
    path('mailinglists/create/', MailingListCreateView.as_view(), name='mailinglist-create'),
    path('mailinglists/<int:pk>/update/', MailingListUpdateView.as_view(), name='mailinglist-update'),
    path('mailinglists/<int:pk>/delete/', MailingListDeleteView.as_view(), name='mailinglist-delete'),
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('clients/create/', ClientCreateView.as_view(), name='client-create'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client-update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),
]