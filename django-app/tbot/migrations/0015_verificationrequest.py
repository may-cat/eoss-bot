# Generated by Django 4.0.4 on 2022-06-09 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tbot', '0014_alter_user_dialog_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.TextField(default='')),
                ('flat', models.TextField(default='')),
                ('parking', models.TextField(default='')),
                ('storeroom', models.TextField(default='')),
                ('commerce', models.TextField(default='')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tbot.user')),
            ],
        ),
    ]
