# Generated by Django 3.0.8 on 2020-07-28 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts_app', '0003_rolemapping'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='role_id',
        ),
    ]
