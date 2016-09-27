# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-30 22:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type', models.CharField(choices=[(b'H', b'home'), (b'W', b'work')], default=b'H', max_length=1)),
                ('street_address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('party', models.CharField(blank=True, max_length=100)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('volunteer', models.BooleanField(default=True)),
                ('contact_after', models.DateTimeField(blank=True, null=True)),
                ('contact_before', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('phone_type', models.CharField(choices=[(b'H', b'home'), (b'C', b'cell'), (b'W', b'work'), (b'M', b'main')], default=b'C', max_length=1)),
                ('number', models.CharField(max_length=32)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='phones',
            field=models.ManyToManyField(to='volunteers.PhoneNumber'),
        ),
        migrations.AddField(
            model_name='location',
            name='contact',
            field=models.ManyToManyField(to='volunteers.Person'),
        ),
        migrations.AddField(
            model_name='location',
            name='phones',
            field=models.ManyToManyField(to='volunteers.PhoneNumber'),
        ),
        migrations.AddField(
            model_name='address',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='volunteers.Location'),
        ),
        migrations.AddField(
            model_name='address',
            name='person',
            field=models.ManyToManyField(to='volunteers.Person'),
        ),
    ]
