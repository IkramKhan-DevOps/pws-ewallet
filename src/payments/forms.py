from django.forms import ModelForm
from src.payments.models import Connect, ExternalAccount


class ConnectCreateForm(ModelForm):
    class Meta:
        model = Connect
        fields = [
            'first_name', 'last_name', 'phone', 'country', 'city', 'currency', 'postal_code', 'address'
        ]


class ConnectUpdateForm(ModelForm):
    class Meta:
        model = Connect
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'city', 'postal_code', 'address'
        ]


class ExternalAccountCreateForm(ModelForm):
    class Meta:
        model = ExternalAccount
        fields = [
            'country', 'currency', 'account_holder_name', 'routing_number', 'account_number'
        ]


class ExternalAccountUpdateForm(ModelForm):
    class Meta:
        model = ExternalAccount
        fields = [
            'country', 'currency', 'account_holder_name', 'routing_number', 'account_number'
        ]

