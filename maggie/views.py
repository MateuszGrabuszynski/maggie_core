from django.shortcuts import render
from django.contrib.auth import mixins
from django.views.generic import edit, detail, list

from . import models

class TransactionsListView(mixins.LoginRequiredMixin, list.ListView):
    model = models.Transaction
    paginate_by = 100
    context_object_name = 'transactions'
    list_title = None


class HomeView(TransactionsListView):
    list_title = 'All transactions'
