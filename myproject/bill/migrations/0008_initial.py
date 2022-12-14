# Generated by Django 4.1.2 on 2022-10-21 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("bill", "0007_delete_bill"),
    ]

    operations = [
        migrations.CreateModel(
            name="Bill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.IntegerField()),
                ("source_type", models.CharField(max_length=255)),
                ("bill_amount", models.IntegerField()),
                ("category_type", models.CharField(max_length=255)),
                ("category_id", models.IntegerField()),
                ("bill_remark", models.CharField(max_length=255, null=True)),
                ("bill_date", models.CharField(max_length=255)),
            ],
        ),
    ]
