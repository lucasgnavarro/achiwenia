# Generated by Django 2.1.7 on 2019-04-18 22:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0010_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(blank=None, max_length=120, null=True)),
                ('number', models.CharField(blank=None, max_length=35, null=True)),
                ('floor', models.CharField(blank=True, default='', max_length=35)),
                ('room_number', models.CharField(blank=True, default='', max_length=4)),
                ('is_physical', models.BooleanField(default=False)),
                ('is_shipping', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='auth.UserProfile')),
            ],
            options={
                'verbose_name': 'User Address',
                'verbose_name_plural': 'User Addresses',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.CharField(editable=False, max_length=3, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=60)),
            ],
        ),
    ]