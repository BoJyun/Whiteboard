# Generated by Django 3.1 on 2021-01-07 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whiteboard', '0003_people_circulenum'),
    ]

    operations = [
        migrations.AddField(
            model_name='people',
            name='DownTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]