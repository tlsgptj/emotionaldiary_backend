# Generated by Django 5.1 on 2024-11-14 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='additional_field',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
