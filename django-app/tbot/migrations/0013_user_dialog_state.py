# Generated by Django 4.0.4 on 2022-05-15 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tbot', '0012_remove_estate_users_and_weights'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='dialog_state',
            field=models.CharField(default='', max_length=255),
        ),
    ]
