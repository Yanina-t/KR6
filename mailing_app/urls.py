from django.urls import path
from django.views.decorators.cache import cache_page

from mailing_app.apps import MailingAppConfig
from .views import (MailingServiceDetailView, MailingServiceCreateView, MailingServiceUpdateView,
                    MailingServiceDeleteView, ClientCreateView, ClientListView, ClientUpdateView,
                    ClientDeleteView, ClientDetailView, DeliveryLogListView,
                    MailingServiceListView, home)

app_name = MailingAppConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('mailinglists', MailingServiceListView.as_view(), name='mailingservice-list'),
    path('mailinglists/<int:pk>/', cache_page(60)(MailingServiceDetailView), name='mailingservice-detail'),
    path('mailinglists/create/', MailingServiceCreateView.as_view(), name='mailingservice-create'),
    path('mailinglists/<int:pk>/update/', MailingServiceUpdateView.as_view(), name='mailingservice-update'),
    path('mailinglists/<int:pk>/delete/', MailingServiceDeleteView.as_view(), name='mailingservice-delete'),
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('clients/<int:pk>/', cache_page(60)(ClientDetailView), name='client-detail'),
    path('clients/create/', ClientCreateView.as_view(), name='client-create'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client-update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),
    path('log', DeliveryLogListView.as_view(), name='log_list'),

]
