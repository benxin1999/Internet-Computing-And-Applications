# Generated by Django 4.1.2 on 2022-10-25 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bill", "0010_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="category_name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
