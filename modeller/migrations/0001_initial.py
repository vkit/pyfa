# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-05 07:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelField',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.SlugField(blank=True)),
                ('field_type', models.IntegerField(blank=True, choices=[(1, 'AutoField'), (2, 'IntegerField'), (3, 'FloatField'), (4, 'DateField'), (5, 'DateTimeField'), (6, 'EmailField'), (7, 'TimeField'), (8, 'DecimalField'), (9, 'CharField'), (10, 'SlugField'), (11, 'TextField'), (12, 'URLField'), (13, 'BigIntegerField'), (14, 'SmallIntegerField'), (15, 'PositiveSmallIntegerField'), (16, 'BooleanField'), (17, 'ForeignKey'), (18, 'ManyToManyField'), (19, 'OneToOneField'), (20, 'DurationField')])),
                ('max_length', models.IntegerField(blank=True, null=True)),
                ('default', models.CharField(blank=True, max_length=50, null=True)),
                ('blank', models.BooleanField(default=False)),
                ('null', models.BooleanField(default=False)),
                ('unique', models.BooleanField(default=False)),
                ('foreign_key', models.CharField(blank=True, max_length=100, null=True)),
                ('many_to_many_key', models.CharField(blank=True, max_length=50, null=True)),
                ('related_name', models.CharField(blank=True, max_length=50, null=True)),
                ('max_digits', models.IntegerField(blank=True, null=True)),
                ('decimal_places', models.IntegerField(blank=True, null=True)),
                ('choices', models.CharField(blank=True, help_text="Add a Python Tupple ((1, 'Today'),(2, 'Tomorrow'),", max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='ModelObject',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.SlugField(blank=True, unique=True)),
                ('inherit', models.CharField(max_length=20)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.App')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='modelfield',
            name='model_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modeller.ModelObject'),
        ),
        migrations.AlterUniqueTogether(
            name='modelfield',
            unique_together=set([('name', 'model_obj')]),
        ),
    ]