# Generated by Django 3.2.9 on 2023-02-23 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0012_userchoice_solved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userchoice',
            name='solved',
        ),
    ]
