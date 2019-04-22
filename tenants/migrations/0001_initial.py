# Generated by Django 2.1.7 on 2019-04-18 22:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatabaseServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('engine', models.CharField(blank=None, choices=[('django.db.backends.postgresql', 'Postgresql')], default='Postgresql', max_length=50)),
                ('host', models.CharField(default='127.0.0.1', max_length=60)),
                ('port', models.IntegerField(default=5432)),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_name', models.CharField(default='', max_length=255)),
                ('db_user', models.CharField(default='', max_length=255)),
                ('db_password', models.CharField(default='', max_length=255)),
                ('options', models.CharField(default='', max_length=255)),
                ('alias', models.CharField(default='', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='applications.Application')),
                ('db_server', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tenants.DatabaseServer')),
            ],
        ),
    ]