# Generated by Django 3.2.5 on 2022-03-31 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('pwd', models.CharField(max_length=32)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('key', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='DateInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('site', models.URLField(max_length=32)),
                ('account', models.CharField(max_length=32)),
                ('password', models.BinaryField(max_length=128)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('userinfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.userinfo')),
            ],
        ),
    ]
