from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import MailingServiceForm, ClientForm, MessageForm
from .models import MailingService, Client, Message, DeliveryLog


class HomeView(View):
    template_name = 'mailing_app/home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class MailingServiceListView(ListView):
    model = MailingService

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['all'] = context_data['object_list'].count()
        context_data['active'] = context_data['object_list'].filter(status=MailingService.STARTED).count()

        mailing_list = context_data['object_list'].prefetch_related('clients')
        clients = set()
        [[clients.add(client.email) for client in mailing.clients.all()] for mailing in mailing_list]
        context_data['clients_count'] = len(clients)
        return context_data


# class MailingListView(ListView):
#     model = MailingList
#     template_name = 'mailing_app/mailinglist_list.html'
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super().get_context_data(*args, **kwargs)
#
#         context_data['all'] = context_data['object_list'].count()
#         context_data['active'] = context_data['object_list'].filter(status=MailingList.STARTED).count()
#
#         mailing_list = context_data['object_list'].prefetch_related('clients')
#         clients = set()
#         [[clients.add(client.email) for client in mailing.clients.all()] for mailing in mailing_list]
#         context_data['clients_count'] = len(clients)
#         return context_data


class MailingServiceDetailView(DetailView):
    model = MailingService
    # template_name = 'mailing_app/mmailingservice1_detail.html'
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['messages'] = self.object.message.all()
    #     context['logs'] = self.object.deliverylog_set.all()
    #     return context


class MailingServiceCreateView(CreateView):
    model = MailingService
    form_class = MailingServiceForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(MailingService, Message, extra=1, form=MessageForm)

        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST)
        else:
            context_data['formset'] = MessageFormset()

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing_app:mailingservice-list')


class MailingServiceUpdateView(UpdateView):
    model = MailingService
    form_class = MailingServiceForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(MailingService, Message, extra=1, form=MessageForm)

        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MessageFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing_app:mailingservice-list')


class MailingServiceDeleteView(DeleteView):
    model = MailingService
    template_name = 'mailing_app/mailingservice_delete.html'

    def get_success_url(self):
        return reverse('mailing_app:mailingservice-list')


class ClientListView(ListView):
    model = Client
    template_name = 'mailing_app/client_list.html'
    context_object_name = 'object_list'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing_app/client_detail.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing_app:client-list')  # Redirect after deletion


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mailing_app:client-list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing_app/client_confirm_delete.html'
    success_url = '/clients/'  # Redirect after deletion


class DeliveryLogListView(ListView):
    model = DeliveryLog

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['all'] = context_data['object_list'].count()
        context_data['success'] = context_data['object_list'].filter(status=True).count()
        context_data['error'] = context_data['object_list'].filter(status=False).count()

        return context_data


#
# class MessageListView(ListView):
#     model = Message
#     template_name = 'mailing_app/message_list.html'
#     context_object_name = 'object_m_list'
#
#
# class MessageDetailView(DetailView):
#     model = Message
#     template_name = 'mailing_app/message_detail.html'
#
#
# class MessageCreateView(CreateView):
#     model = Message
#     form_class = MessageForm
#     success_url = '/message/'
#
#
# class MessageUpdateView(UpdateView):
#     model = Message
#     template_name = 'mailing_app/message_form.html'
#     form_class = MessageForm
#     success_url = '/message/'
#
#
# class MessageDeleteView(DeleteView):
#     model = Message
#     template_name = 'mailing_app/message_confirm_delete.html'
#     success_url = '/message/'  # Redirect after deletion

