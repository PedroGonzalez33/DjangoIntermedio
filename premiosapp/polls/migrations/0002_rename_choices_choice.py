# Generated by Django 4.2.3 on 2023-07-05 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Choices",
            new_name="Choice",
        ),
    ]
