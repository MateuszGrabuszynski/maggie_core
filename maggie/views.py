from django.shortcuts import render
from django.contrib.auth import mixins
from django.views.generic import edit, detail, list

from . import forms
from . import models

class ListTransactionsView(mixins.LoginRequiredMixin, list.ListView):
    model = models.Transaction
    paginate_by = 100
    context_object_name = 'transactions'
    list_title = 'All transactions'


class AddTransactionView(mixins.LoginRequiredMixin, edit.CreateView):
    model = models.Transaction
    form_class = forms.AddTransactionForm


class DetailedTransactionView(mixins.LoginRequiredMixin, detail.DetailView):
    model = models.Transaction
