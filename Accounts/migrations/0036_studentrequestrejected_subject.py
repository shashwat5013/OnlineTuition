# Generated by Django 3.0.8 on 2020-09-03 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0035_auto_20200903_0655'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentrequestrejected',
            name='subject',
            field=models.CharField(default=' ', max_length=254),
        ),
    ]