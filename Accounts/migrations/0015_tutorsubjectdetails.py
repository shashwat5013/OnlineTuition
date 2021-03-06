# Generated by Django 3.0.8 on 2020-08-04 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0014_delete_tutorsubjectdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='tutorSubjectDetails',
            fields=[
                ('emailId', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('subjectName1', models.CharField(max_length=100, null=True)),
                ('subjectName2', models.CharField(max_length=100, null=True)),
                ('subjectName3', models.CharField(max_length=100, null=True)),
                ('hourlyPrice1', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('phoneNumber', models.CharField(max_length=20, null=True)),
                ('summary', models.CharField(max_length=10000, null=True)),
            ],
        ),
    ]
