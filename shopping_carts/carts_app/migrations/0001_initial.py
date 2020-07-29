# Generated by Django 3.0.8 on 2020-07-28 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_id', models.AutoField(primary_key=True, serialize=False)),
                ('role_name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=100)),
                ('user_name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('role_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts_app.Role')),
            ],
        ),
        migrations.CreateModel(
            name='Carts',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
                ('count', models.IntegerField()),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts_app.Item')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts_app.User')),
            ],
        ),
    ]
