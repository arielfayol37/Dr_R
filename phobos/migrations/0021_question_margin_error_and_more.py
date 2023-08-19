# Generated by Django 4.2.3 on 2023-08-19 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phobos', '0020_question_max_num_attempts'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='margin_error',
            field=models.FloatField(blank=True, default=0.03, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='deduct_per_attempt',
            field=models.FloatField(blank=True, default=0.05, null=True),
        ),
    ]
