# Generated by Django 4.2.3 on 2023-09-22 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phobos', '0033_merge_20230921_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='is_assigned',
            field=models.BooleanField(default=False),
        ),
    ]
