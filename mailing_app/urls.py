from django.urls import path
from mailing_app.apps import MailingAppConfig
from .views import (MailingServiceDetailView, MailingServiceCreateView, MailingServiceUpdateView,
                    MailingServiceDeleteView, ClientCreateView, ClientListView, ClientUpdateView,
                    ClientDeleteView, ClientDetailView, DeliveryLogListView,
                    MailingServiceListView, HomeView)

app_name = MailingAppConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('mailinglists', MailingServiceListView.as_view(), name='mailingservice-list'),
    path('mailinglists/<int:pk>/', MailingServiceDetailView.as_view(), name='mailingservice-detail'),
    path('mailinglists/create/', MailingServiceCreateView.as_view(), name='mailingservice-create'),
    path('mailinglists/<int:pk>/update/', MailingServiceUpdateView.as_view(), name='mailingservice-update'),
    path('mailinglists/<int:pk>/delete/', MailingServiceDeleteView.as_view(), name='mailingservice-delete'),
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('clients/create/', ClientCreateView.as_view(), name='client-create'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client-update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),
    path('log', DeliveryLogListView.as_view(), name='log_list'),

]
