from django.contrib import admin

from app.views import client
from .models import Client, Transaction, Vendor, Stock

# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "created_at",
        "updated_at",
    )
    search_fields = ("name","phone")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "created_at",
        "updated_at",
    )
    search_fields = ("customer",)


admin.site.register(Vendor)

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        "supplier",
        "created_at",
        "updated_at",
    )
    search_fields = ("supplier",)