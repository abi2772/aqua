from venv import create
from django.db import models

# Create your models here.
class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Client(Base):
    class Meta:
        ordering = ("-created_at",)

    name = models.CharField(max_length=124)
    phone = models.CharField(max_length=11)
    address = models.TextField()
    equipement = models.CharField(max_length=225)
    installation = models.DateTimeField(blank=True, null=True)
    service = models.DateTimeField(blank=True, null=True)
    maintenace = models.DateTimeField(blank=True, null=True)
    staff = models.CharField(max_length=255,blank=True, null=True)

    def __str__ (self):
        return self.name


class Transaction(Base):
    class Meta:
        ordering = ("-created_at",)

    customer = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="transactions")
    debit = models.FloatField(blank=True, null=True, default=0.0)
    credit = models.FloatField(blank=True, null=True, default=0.0)
    service_type = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=225)

class Vendor(Base):
    class Meta:
        ordering = ("-created_at",)

    name = models.CharField(max_length=124)
    phone = models.CharField(max_length=11)
    address = models.TextField()

    def __str__ (self):
        return self.name

class Stock(Base):
    supplier = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="stocks")
    item = models.CharField(max_length=255, blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    pay = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)

    def total_amount(self):
        return self.price * self.qty

class Expense(Base):
    detail = models.CharField(max_length=255)
    amount = models.FloatField()