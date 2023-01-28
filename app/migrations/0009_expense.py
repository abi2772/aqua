# Generated by Django 4.1 on 2022-09-03 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0008_alter_stock_supplier"),
    ]

    operations = [
        migrations.CreateModel(
            name="Expense",
            fields=[
                (
                    "base_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="app.base",
                    ),
                ),
                ("detail", models.CharField(max_length=255)),
                ("amount", models.FloatField()),
            ],
            bases=("app.base",),
        ),
    ]