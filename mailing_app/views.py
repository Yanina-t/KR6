import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Blog
from .forms import MailingServiceForm, ClientForm, MessageForm
from .models import MailingService, Client, DeliveryLog, Message
from django.views.decorators.cache import cache_page

@login_required
def home(request):
    # Получите набор данных на основе ваших потребностей
    mailing_services = MailingService.objects.all()
    # Рассчитайте количество
    all_count = mailing_services.count()
    active_count = mailing_services.filter(status=MailingService.STARTED).count()
    # Рассчитать clients_count (всех клиентов, независимо от пользователя)
    clients_count = Client.objects.count()
    # Получите три случайные статьи блога
    all_articles = Blog.objects.all()
    random_articles = random.sample(list(all_articles), min(3, all_articles.count()))

    for article in random_articles:
        article.views_count += 1
        article.save()

    context = {
            'all': all_count,
            'active': active_count,
            'clients_count': clients_count,
            'random_articles': random_articles,
        }

    # Верните шаблон с контекстом
    return render(request, 'mailing_app/home.html', context)


class MailingServiceListView(LoginRequiredMixin, ListView):
    model = MailingService

    def get_queryset(self):
        if self.request.user.is_moderator:
            # Если пользователь - модератор, показать все рассылки
            return MailingService.objects.all()
        else:
            # Иначе, показать только рассылки, принадлежащие текущему пользователю
            return MailingService.objects.filter(user_mailing=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['all'] = context_data['object_list'].count()
        context_data['active'] = context_data['object_list'].filter(status=MailingService.STARTED).count()

        mailing_list = context_data['object_list'].prefetch_related('clients')
        clients = set()
        [[clients.add(client.email) for client in mailing.clients.all()] for mailing in mailing_list]
        context_data['clients_count'] = len(clients)
        return context_data


class MailingServiceDetailView(DetailView):
    model = MailingService


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

        # Передача текущего пользователя в форму рассылки и формсет
        context_data['form'].user_mailing = self.request.user
        context_data['formset'].user_mailing = self.request.user

        return context_data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_mailing = self.request.user
        formset = self.get_context_data()['formset']

        if form.is_valid():
            self.object.save()

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


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailing_app/client_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        # Возвращает только клиентов, принадлежащие текущему пользователю
        return Client.objects.filter(user_client=self.request.user)


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing_app/client_detail.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_client = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing_app:client-list')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mailing_app:client-list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing_app/client_confirm_delete.html'
    success_url = '/clients/'  # Redirect after deletion


class DeliveryLogListView(LoginRequiredMixin, ListView):
    model = DeliveryLog

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['all'] = context_data['object_list'].count()
        context_data['success'] = context_data['object_list'].filter(status=True).count()
        context_data['error'] = context_data['object_list'].filter(status=False).count()

        return context_data
