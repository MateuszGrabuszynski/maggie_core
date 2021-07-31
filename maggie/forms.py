from django import forms

from . import models


class AddTransactionForm(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = ('name', 'sender', 'recipient', 'product',)
