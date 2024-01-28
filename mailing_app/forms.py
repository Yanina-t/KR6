from django.forms import ModelForm
from .models import MailingList, Message, Client


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingListForm(StyleFormMixin, ModelForm):
    class Meta:
        model = MailingList
        fields = ('send_time', 'end_time', 'frequency', 'status', 'clients',)


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = ['name_letter', 'subject', 'body']


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']

