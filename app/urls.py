from django.urls import path
from django.contrib.auth import views as auth_views
from .views import delete_client, index, client, client_new, info, transaction, vendor, vendordetail, vendortransaction, reminder, expense, invoice, search, paid_by_client, delete_client
urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('index/', index, name="home"),
    path('client/', client, name="client"),
    path('add/', client_new, name="add"),
    path('info/<int:id>/', info, name="info"),
    path('transaction/', transaction, name="transaction"),
    path('vendor/', vendor, name="vendor"),
    path('vendor-detail/<int:id>/', vendordetail, name="vendor-detail"),
    path('vendor-transaction/', vendortransaction, name="vendor-transaction"),
    path('reminder/', reminder, name="reminder"),
    path('expense/', expense, name="expense"),
    path('invoice/', invoice, name="invoice"),
    path('search/', search, name="search"),
    path('paid_by_client/', paid_by_client, name="paid_by_client"),
    path('delete/<int:id>/', delete_client, name="delete"),

]