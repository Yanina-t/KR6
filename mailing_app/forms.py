from django.forms import ModelForm
from .models import MailingService, Message, Client


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingServiceForm(StyleFormMixin, ModelForm):
    class Meta:
        model = MailingService
        fields = ('send_time', 'end_time', 'frequency', 'status', 'clients',)

    def __init__(self, *args, **kwargs):
        self.user_mailing = kwargs.pop('user_mailing', None)
        super().__init__(*args, **kwargs)
        if self.user_mailing:
            # Фильтрация клиентов только для текущего пользователя
            self.fields['clients'].queryset = Client.objects.filter(user=self.user_mailing)


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']

