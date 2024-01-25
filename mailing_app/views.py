from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import MailingListForm, MessageForm, ClientForm
from .models import MailingList, Client, Message, DeliveryLog


class HomeView(View):
    template_name = 'mailing_app/home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class MailingListView(ListView):
    model = MailingList
    template_name = 'mailing_app/mailinglist_list.html'


class MailingListDetailView(DetailView):
    model = MailingList
    template_name = 'mailing_app/mailinglist_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.object.message_set.all()
        context['logs'] = self.object.deliverylog_set.all()
        return context


class MailingListCreateView(View):
    def post(self, request):
        mailing_form = MailingListForm(request.POST)
        message_form = MessageForm(request.POST)

        if mailing_form.is_valid() and message_form.is_valid():
            mailing_list = mailing_form.save()
            message = message_form.save(commit=False)
            message.mailing_list = mailing_list
            message.save()

            # Create delivery log entry
            DeliveryLog.objects.create(message=message, status='Sent')

            return redirect('mailinglist-list')

        return render(request, 'mailing_app/mailinglist_create.html', {'mailing_form': mailing_form, 'message_form': message_form})


class MailingListUpdateView(UpdateView):
    model = MailingList
    template_name = 'mailing_app/mailinglist_form.html'
    fields = ['send_time', 'frequency', 'status']
    success_url = '/mailinglists/'


class MailingListDeleteView(DeleteView):
    model = MailingList
    template_name = 'mailing_app/mailinglist_confirm_delete.html'
    success_url = reverse_lazy('mailinglist-list') # Redirect after deletion


class ClientListView(ListView):
    model = Client
    template_name = 'mailing_app/client_list.html'
    context_object_name = 'object_list'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing_app/client_detail.html'


class ClientCreateView(View):
    def get(self, request):
        client_form = ClientForm()
        return render(request, 'mailing_app/client_create.html', {'client_form': client_form})

    def post(self, request):
        client_form = ClientForm(request.POST)

        if client_form.is_valid():
            client_form.save()
            return redirect('client-list')  # Перенаправление на список клиентов или другую страницу

        return render(request, 'mailing_app/client_create.html', {'client_form': client_form})


class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'mailing_app/client_form.html'
    form_class = ClientForm
    success_url = '/clients/'


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing_app/client_confirm_delete.html'
    success_url = '/clients/'  # Redirect after deletion

