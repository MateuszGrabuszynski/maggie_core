from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListTransactionsView.as_view(), name='transaction_list'),
    path('add', views.AddTransactionView.as_view(), name='transaction_add'),
    path('<int:pk>', views.DetailedTransactionView.as_view(), name='transaction_detail')
]