# Generated by Django 4.0.4 on 2022-04-22 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbot', '0007_user_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='estate',
        ),
        migrations.DeleteModel(
            name='Eossstats',
        ),
    ]
