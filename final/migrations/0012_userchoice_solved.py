# Generated by Django 3.2.9 on 2023-02-23 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0011_cards_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='userchoice',
            name='solved',
            field=models.BooleanField(default=True),
        ),
    ]
