from django import forms
from .models import MailingList, Message, DeliveryLog, Client


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']


class MailingListForm(forms.ModelForm):
    class Meta:
        model = MailingList
        fields = ['send_time', 'frequency', 'status']

    send_time = forms.DateTimeField(
        widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )


class DeliveryLogForm(forms.ModelForm):
    class Meta:
        model = DeliveryLog
        fields = ['status', 'server_response']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']
